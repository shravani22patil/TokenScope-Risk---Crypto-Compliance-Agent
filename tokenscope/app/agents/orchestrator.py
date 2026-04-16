"""
agents/orchestrator.py
-----------------------
TokenScope Risk — Multi-step AI agent workflow.

Agents run sequentially, each building on the previous state.
Each agent calls Claude with a focused, structured prompt and returns
typed output — no single mega-prompt.

Agents:
  1. IntakeAgent       — validates + classifies inputs
  2. ResearchAgent     — scrapes web sources
  3. DocumentAgent     — parses whitepaper / docs
  4. GitHubAgent       — fetches repo signals
  5. RiskReviewAgent   — identifies red flags via LLM
  6. ScoringAgent      — computes dimension scores
  7. MemoWriterAgent   — generates executive memo
"""

from __future__ import annotations
import json
import os
import uuid
from datetime import datetime
from typing import Any, Callable, Optional

import anthropic

from ..services.scraper import fetch_url_text, fetch_pdf_text, fetch_github_signals
from ..models.schemas import AnalysisRequest

# Initialize client lazily
_client: Optional[anthropic.Anthropic] = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def _claude(system: str, user: str, max_tokens: int = 1200) -> str:
    """Single Claude call. Returns text content."""
    try:
        msg = _get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        return f"[LLM ERROR: {e}]"


def _parse_json_response(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences."""
    import re
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        # Last resort: return a minimal dict
        return {"parse_error": text[:500]}


# ─────────────────────────────────────────────────────────────────────────────
# State object passed between agents
# ─────────────────────────────────────────────────────────────────────────────

class AgentState:
    def __init__(self, request: AnalysisRequest):
        self.request = request
        self.steps_log: list[str] = []
        self.sources: list[dict] = []
        self.raw_texts: dict[str, str] = {}       # source_type -> extracted text
        self.github_signals: Optional[dict] = None
        self.red_flags: list[dict] = []
        self.credibility_indicators: list[str] = []
        self.missing_information: list[str] = []
        self.project_summary: str = ""
        self.token_utility_summary: str = ""
        self.extracted_metadata: dict = {}
        self.scoring: dict = {}
        self.executive_summary: str = ""
        self.analyst_notes: str = ""

    def log(self, msg: str, progress_cb: Optional[Callable] = None) -> None:
        self.steps_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        if progress_cb:
            progress_cb(msg)

    def source_coverage_pct(self) -> float:
        possible = 4  # website, whitepaper, github, docs
        fetched = sum(1 for s in self.sources if s["status"] == "fetched")
        return (fetched / possible) * 100


# ─────────────────────────────────────────────────────────────────────────────
# Agent 1 — Intake
# ─────────────────────────────────────────────────────────────────────────────

def intake_agent(state: AgentState, progress_cb=None) -> AgentState:
    state.log("Intake Agent: Validating inputs...", progress_cb)
    req = state.request
    missing = []
    if not req.website_url:
        missing.append("website_url")
    if not req.whitepaper_url:
        missing.append("whitepaper / litepaper URL")
    if not req.github_url:
        missing.append("GitHub repository URL")
    if not req.docs_url:
        missing.append("documentation URL")
    state.missing_information = missing
    state.log(f"Intake: {len(missing)} sources missing: {missing}", progress_cb)
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Agent 2 — Research (web scraping)
# ─────────────────────────────────────────────────────────────────────────────

def research_agent(state: AgentState, progress_cb=None) -> AgentState:
    req = state.request

    urls = {
        "website": req.website_url,
        "docs": req.docs_url,
    }

    for src_type, url in urls.items():
        if not url:
            state.sources.append({
                "source_type": src_type,
                "url": None,
                "status": "skipped",
                "raw_excerpt": None,
                "full_text_length": 0,
                "fetch_error": "URL not provided",
            })
            continue

        state.log(f"Research Agent: Fetching {src_type} → {url}", progress_cb)
        text, err = fetch_url_text(url)
        if err or not text:
            state.sources.append({
                "source_type": src_type,
                "url": url,
                "status": "failed",
                "raw_excerpt": None,
                "full_text_length": 0,
                "fetch_error": err or "Empty response",
            })
        else:
            state.raw_texts[src_type] = text
            state.sources.append({
                "source_type": src_type,
                "url": url,
                "status": "fetched",
                "raw_excerpt": text[:600],
                "full_text_length": len(text),
                "fetch_error": None,
            })
            state.log(f"Research Agent: {src_type} fetched ({len(text)} chars)", progress_cb)

    return state


# ─────────────────────────────────────────────────────────────────────────────
# Agent 3 — Document (whitepaper PDF)
# ─────────────────────────────────────────────────────────────────────────────

def document_agent(state: AgentState, progress_cb=None) -> AgentState:
    url = state.request.whitepaper_url
    if not url:
        state.sources.append({
            "source_type": "whitepaper",
            "url": None,
            "status": "skipped",
            "raw_excerpt": None,
            "full_text_length": 0,
            "fetch_error": "No whitepaper URL provided",
        })
        return state

    state.log(f"Document Agent: Parsing whitepaper → {url}", progress_cb)

    # Try as PDF first, fallback to HTML
    text, err = fetch_pdf_text(url)
    if not text:
        text, err = fetch_url_text(url)

    if text:
        state.raw_texts["whitepaper"] = text
        state.sources.append({
            "source_type": "whitepaper",
            "url": url,
            "status": "fetched",
            "raw_excerpt": text[:600],
            "full_text_length": len(text),
            "fetch_error": None,
        })
        state.log(f"Document Agent: Whitepaper parsed ({len(text)} chars)", progress_cb)
    else:
        state.sources.append({
            "source_type": "whitepaper",
            "url": url,
            "status": "failed",
            "raw_excerpt": None,
            "full_text_length": 0,
            "fetch_error": err or "Failed to extract text",
        })

    return state


# ─────────────────────────────────────────────────────────────────────────────
# Agent 4 — GitHub
# ─────────────────────────────────────────────────────────────────────────────

def github_agent(state: AgentState, progress_cb=None) -> AgentState:
    url = state.request.github_url
    if not url:
        state.sources.append({
            "source_type": "github",
            "url": None,
            "status": "skipped",
            "raw_excerpt": None,
            "full_text_length": 0,
            "fetch_error": "No GitHub URL provided",
        })
        return state

    state.log(f"GitHub Agent: Fetching repo signals → {url}", progress_cb)
    signals = fetch_github_signals(url)
    state.github_signals = signals

    status = "fetched" if signals.get("stars") is not None else "failed"
    err = signals["notes"][0] if signals["notes"] and status == "failed" else None
    state.sources.append({
        "source_type": "github",
        "url": url,
        "status": status,
        "raw_excerpt": None,
        "full_text_length": 0,
        "fetch_error": err,
    })
    state.log(f"GitHub Agent: {signals.get('signal_strength','?')} signal, {signals.get('stars','?')} stars", progress_cb)
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Agent 5 — Risk Review (LLM-powered red flag detection)
# ─────────────────────────────────────────────────────────────────────────────

RISK_SYSTEM = """You are a senior crypto compliance analyst at a major exchange.
Your job is to identify red flags and credibility signals in token/project research data.
Be critical, specific, and evidence-backed. Never hallucinate — only flag what the text shows.
Respond ONLY in valid JSON, no markdown fences, no preamble."""

def risk_review_agent(state: AgentState, progress_cb=None) -> AgentState:
    state.log("Risk Review Agent: Analyzing for red flags...", progress_cb)

    # Compile all source text into one context block
    context_parts = []
    for src_type, text in state.raw_texts.items():
        context_parts.append(f"=== SOURCE: {src_type.upper()} ===\n{text[:3000]}")
    context = "\n\n".join(context_parts) if context_parts else "NO SOURCE TEXT AVAILABLE"

    prompt = f"""Project: {state.request.project_name}
Ticker: {state.request.token_ticker or 'unknown'}
Extra notes: {state.request.extra_notes or 'none'}

Source content collected:
{context}

Analyze the above and respond with this exact JSON structure:
{{
  "project_summary": "2-4 sentence objective summary of the project",
  "token_utility_summary": "2-3 sentence summary of token utility and mechanics",
  "extracted_metadata": {{
    "founded": "year or unknown",
    "team_size_disclosed": "number or unknown",
    "audits_mentioned": "yes/no/unknown",
    "mainnet_status": "live/testnet/unknown"
  }},
  "red_flags": [
    {{"category": "string", "description": "specific evidence-backed description", "severity": "high|medium|low", "source_reference": "which source"}}
  ],
  "credibility_indicators": ["list of positive signals found"],
  "missing_information": ["list of missing but important information"]
}}"""

    raw = _claude(RISK_SYSTEM, prompt, max_tokens=1500)
    parsed = _parse_json_response(raw)

    state.project_summary = parsed.get("project_summary", "Unable to extract project summary.")
    state.token_utility_summary = parsed.get("token_utility_summary", "Unable to extract token utility.")
    state.extracted_metadata = parsed.get("extracted_metadata", {})
    state.red_flags = parsed.get("red_flags", [])
    state.credibility_indicators = parsed.get("credibility_indicators", [])
    # Merge with intake-detected missing
    llm_missing = parsed.get("missing_information", [])
    state.missing_information = list(set(state.missing_information + llm_missing))

    state.log(f"Risk Review Agent: {len(state.red_flags)} red flags, {len(state.credibility_indicators)} credibility signals", progress_cb)
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Agent 6 — Scoring
# ─────────────────────────────────────────────────────────────────────────────

SCORING_SYSTEM = """You are a crypto risk scoring engine.
Given project research data, compute dimension-wise scores precisely.
Base scores on evidence provided — never invent facts.
Respond ONLY in valid JSON. No markdown. No commentary outside JSON."""

def scoring_agent(state: AgentState, progress_cb=None) -> AgentState:
    state.log("Scoring Agent: Computing risk dimensions...", progress_cb)

    gh = state.github_signals or {}
    flags_summary = "\n".join(f"- [{f.get('severity','?')}] {f.get('description','')}" for f in state.red_flags[:10])
    cred_summary = "\n".join(f"- {c}" for c in state.credibility_indicators[:8])

    prompt = f"""Project: {state.request.project_name}
Project summary: {state.project_summary}
Token utility: {state.token_utility_summary}
Source coverage: {state.source_coverage_pct() if hasattr(state, 'source_coverage_pct') else '?'}%
GitHub: stars={gh.get('stars','none')}, forks={gh.get('forks','none')}, contributors={gh.get('contributor_count','none')}, active={gh.get('is_active', False)}, signal={gh.get('signal_strength','unknown')}
Red flags found:
{flags_summary or 'None'}
Credibility signals:
{cred_summary or 'None'}
Missing sources: {', '.join(state.missing_information[:6]) or 'None'}

Score each dimension. Max scores shown. Be strict.

Respond with this exact JSON:
{{
  "team_transparency": {{"score": 0-20, "max_score": 20, "rationale": "...", "evidence_snippets": []}},
  "documentation_quality": {{"score": 0-15, "max_score": 15, "rationale": "...", "evidence_snippets": []}},
  "token_utility_clarity": {{"score": 0-15, "max_score": 15, "rationale": "...", "evidence_snippets": []}},
  "github_engineering_signal": {{"score": 0-15, "max_score": 15, "rationale": "...", "evidence_snippets": []}},
  "ecosystem_credibility": {{"score": 0-10, "max_score": 10, "rationale": "...", "evidence_snippets": []}},
  "research_completeness": {{"score": 0-10, "max_score": 10, "rationale": "...", "evidence_snippets": []}},
  "hype_penalty": {{"score": -15 to 0, "max_score": 0, "rationale": "...", "evidence_snippets": []}}
}}"""

    raw = _claude(SCORING_SYSTEM, prompt, max_tokens=1200)
    dims = _parse_json_response(raw)

    # Add name field to each dimension
    name_map = {
        "team_transparency": "Team Transparency",
        "documentation_quality": "Documentation Quality",
        "token_utility_clarity": "Token Utility Clarity",
        "github_engineering_signal": "GitHub / Engineering Signal",
        "ecosystem_credibility": "Ecosystem Credibility",
        "research_completeness": "Research Completeness",
        "hype_penalty": "Hype / Inconsistency Penalty",
    }
    for key, name in name_map.items():
        if key in dims:
            dims[key]["name"] = name

    # Compute total
    dimension_keys = list(name_map.keys())
    total = sum(dims.get(k, {}).get("score", 0) for k in dimension_keys)
    total = max(0, total)  # floor at 0 for display

    # Risk level
    if total >= 75:
        risk_level = "strong"
        recommendation = "Strong Initial Signal — Proceed"
    elif total >= 55:
        risk_level = "review"
        recommendation = "Proceed to Deeper Review"
    elif total >= 30:
        risk_level = "medium"
        recommendation = "Monitor — Needs More Data"
    else:
        risk_level = "high"
        recommendation = "High Risk — Do Not List"

    max_possible = 85
    score_pct = (total / max_possible) * 100

    state.scoring = {
        **dims,
        "total_score": total,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "score_breakdown_pct": round(score_pct, 1),
    }

    state.log(f"Scoring Agent: Total={total}/85 → {risk_level.upper()}", progress_cb)
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Agent 7 — Memo Writer
# ─────────────────────────────────────────────────────────────────────────────

MEMO_SYSTEM = """You are a senior analyst writing internal compliance memos for a crypto exchange listings team.
Write in precise, professional language. Be direct. Do not hedge excessively.
Never invent information. Mention what is missing clearly.
Respond ONLY in valid JSON."""

def memo_writer_agent(state: AgentState, progress_cb=None) -> AgentState:
    state.log("Memo Writer Agent: Generating compliance memo...", progress_cb)

    score_info = state.scoring
    total = score_info.get("total_score", 0)
    rec = score_info.get("recommendation", "—")
    risk = score_info.get("risk_level", "—")
    flags = [f.get("description", "") for f in state.red_flags[:5]]
    creds = state.credibility_indicators[:5]

    prompt = f"""Project: {state.request.project_name} ({state.request.token_ticker or '?'})
Risk score: {total}/85 → {risk.upper()}
Recommendation: {rec}
Project summary: {state.project_summary}
Token utility: {state.token_utility_summary}
Top red flags: {json.dumps(flags)}
Credibility signals: {json.dumps(creds)}
Missing information: {json.dumps(state.missing_information[:6])}

Write the executive summary and analyst notes for an internal compliance memo.

Respond with this exact JSON:
{{
  "executive_summary": "3-5 sentence executive summary for listings team",
  "analyst_notes": "1-2 sentence action notes for the analyst"
}}"""

    raw = _claude(MEMO_SYSTEM, prompt, max_tokens=600)
    parsed = _parse_json_response(raw)

    state.executive_summary = parsed.get("executive_summary", state.project_summary)
    state.analyst_notes = parsed.get("analyst_notes", "Review manually.")
    state.log("Memo Writer Agent: Memo complete.", progress_cb)
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Main orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def run_analysis(request: AnalysisRequest, progress_cb=None) -> dict:
    """
    Run all 7 agents sequentially.
    Returns a full report dict ready for storage and display.
    """
    state = AgentState(request)
    state.log("Pipeline started", progress_cb)

    state = intake_agent(state, progress_cb)
    state = research_agent(state, progress_cb)
    state = document_agent(state, progress_cb)
    state = github_agent(state, progress_cb)
    state = risk_review_agent(state, progress_cb)
    state = scoring_agent(state, progress_cb)
    state = memo_writer_agent(state, progress_cb)

    state.log("Pipeline complete", progress_cb)

    report = {
        "report_id": str(uuid.uuid4())[:8],
        "created_at": datetime.utcnow().isoformat(),
        "project_name": request.project_name,
        "token_ticker": request.token_ticker,
        "project_summary": state.project_summary,
        "token_utility_summary": state.token_utility_summary,
        "extracted_metadata": state.extracted_metadata,
        "sources": state.sources,
        "missing_sources": [s["source_type"] for s in state.sources if s["status"] in ("skipped", "failed")],
        "source_coverage_pct": state.source_coverage_pct(),
        "github_signals": state.github_signals,
        "red_flags": state.red_flags,
        "credibility_indicators": state.credibility_indicators,
        "scoring": state.scoring,
        "executive_summary": state.executive_summary,
        "analyst_notes": state.analyst_notes,
        "missing_information": state.missing_information,
        "agent_steps_log": state.steps_log,
        "is_demo": False,
        "demo_scenario": None,
    }
    return report
