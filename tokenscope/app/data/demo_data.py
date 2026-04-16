"""
data/demo_data.py
-----------------
Three pre-built sample reports for demo mode.
Clearly labeled as simulated — no real project partnerships implied.
Scenarios: strong_signal, medium_risk, high_risk
"""

from datetime import datetime
from typing import Any

DEMO_REPORTS: dict[str, dict] = {

    "strong": {
        "report_id": "demo-strong-001",
        "created_at": "2025-10-01T09:00:00",
        "project_name": "Helios Protocol (DEMO)",
        "token_ticker": "HLS",
        "project_summary": (
            "Helios Protocol is a Layer-2 zkRollup network focused on "
            "institutional DeFi settlement. The project has a clearly identified "
            "founding team with doxxed LinkedIn profiles, published academic "
            "backgrounds, and prior experience at Consensys and Ava Labs. "
            "The protocol has been audited by two independent security firms, "
            "with reports publicly available. Tokenomics are clearly defined with "
            "a 4-year vesting schedule and no insider cliff shorter than 12 months."
        ),
        "token_utility_summary": (
            "HLS is used for network fees, governance voting, and validator staking. "
            "Fee burn mechanism creates deflationary pressure. "
            "Utility is well-documented with a formal economic model whitepaper."
        ),
        "extracted_metadata": {
            "founded": "2022",
            "team_size_disclosed": "23",
            "audits_count": "2",
            "mainnet_launch": "Q1 2024",
        },
        "sources": [
            {"source_type": "website", "url": "https://heliosprotocol.io", "status": "simulated", "raw_excerpt": "Helios Protocol — Institutional zkRollup for DeFi settlement. Built by ex-Consensys engineers.", "full_text_length": 4200, "fetch_error": None},
            {"source_type": "whitepaper", "url": "https://heliosprotocol.io/whitepaper.pdf", "status": "simulated", "raw_excerpt": "Section 3: Tokenomics. HLS total supply: 500M. 40% ecosystem, 25% team (4yr vest), 20% investors (1yr cliff), 15% treasury.", "full_text_length": 12000, "fetch_error": None},
            {"source_type": "github", "url": "https://github.com/helios-protocol", "status": "simulated", "raw_excerpt": None, "full_text_length": 0, "fetch_error": None},
            {"source_type": "docs", "url": "https://docs.heliosprotocol.io", "status": "simulated", "raw_excerpt": "Getting started with Helios. The architecture consists of a zkEVM execution layer...", "full_text_length": 8500, "fetch_error": None},
        ],
        "missing_sources": [],
        "source_coverage_pct": 100.0,
        "github_signals": {
            "repo_url": "https://github.com/helios-protocol/core",
            "stars": 1247,
            "forks": 203,
            "open_issues": 18,
            "last_commit_date": "2025-09-28",
            "contributor_count": 34,
            "language": "Rust",
            "is_active": True,
            "signal_strength": "strong",
            "notes": [],
        },
        "red_flags": [
            {"category": "Regulatory", "description": "No explicit compliance officer named in team page", "severity": "low", "source_reference": "website"},
        ],
        "credibility_indicators": [
            "Founding team fully doxxed with verifiable LinkedIn profiles",
            "Two independent security audits published",
            "Mainnet live with >$85M TVL reported",
            "Clear 4-year vesting with 12-month cliff",
            "Active GitHub with 34 contributors and weekly commits",
            "Formal tokenomics whitepaper with economic model",
        ],
        "scoring": {
            "team_transparency": {"name": "Team Transparency", "score": 18, "max_score": 20, "rationale": "Fully doxxed team with verifiable backgrounds.", "evidence_snippets": ["Founding team LinkedIn profiles verified", "Ex-Consensys and Ava Labs backgrounds confirmed"]},
            "documentation_quality": {"name": "Documentation Quality", "score": 14, "max_score": 15, "rationale": "Comprehensive whitepaper and docs. Minor gaps in governance spec.", "evidence_snippets": ["12,000 word whitepaper with economic model", "Full developer docs with API reference"]},
            "token_utility_clarity": {"name": "Token Utility Clarity", "score": 14, "max_score": 15, "rationale": "HLS utility is clearly defined across three use cases with economic rationale.", "evidence_snippets": ["Fee burn mechanism documented", "Staking APY model published"]},
            "github_engineering_signal": {"name": "GitHub / Engineering Signal", "score": 14, "max_score": 15, "rationale": "1,247 stars, 34 contributors, active daily commits.", "evidence_snippets": ["Last commit 3 days ago", "34 public contributors"]},
            "ecosystem_credibility": {"name": "Ecosystem Credibility", "score": 9, "max_score": 10, "rationale": "Mainnet live, notable backers, active community.", "evidence_snippets": ["$85M TVL reported on mainnet"]},
            "research_completeness": {"name": "Research Completeness", "score": 9, "max_score": 10, "rationale": "All 4 source types available and content-rich.", "evidence_snippets": ["All 4 sources fetched successfully"]},
            "hype_penalty": {"name": "Hype / Inconsistency Penalty", "score": -2, "max_score": 0, "rationale": "Minor: marketing copy slightly over-promises on finality speed.", "evidence_snippets": []},
            "total_score": 76,
            "risk_level": "strong",
            "recommendation": "Strong Initial Signal — Proceed",
            "score_breakdown_pct": 89.4,
        },
        "executive_summary": (
            "Helios Protocol presents a strong initial compliance signal. "
            "The team is fully identified, documentation is comprehensive, "
            "engineering activity is healthy, and tokenomics are transparent with "
            "appropriate vesting. Recommend proceeding to deeper legal and financial due diligence."
        ),
        "analyst_notes": "Priority review. Fast-track for legal team. Request audit reports.",
        "missing_information": ["Compliance officer not named on team page"],
        "agent_steps_log": ["[DEMO] Intake validated", "[DEMO] Research complete", "[DEMO] GitHub fetched", "[DEMO] Scoring complete", "[DEMO] Memo written"],
        "is_demo": True,
        "demo_scenario": "strong",
    },

    "medium": {
        "report_id": "demo-medium-001",
        "created_at": "2025-10-01T10:00:00",
        "project_name": "NovaCash Finance (DEMO)",
        "token_ticker": "NVC",
        "project_summary": (
            "NovaCash Finance is a DeFi yield aggregator targeting emerging markets. "
            "The project discloses a partial team — two named founders with LinkedIn profiles "
            "but the remaining 5 team members are identified only by pseudonym. "
            "A litepaper exists but lacks formal economic modeling. "
            "The GitHub has recent activity but contributor count is low (4 contributors)."
        ),
        "token_utility_summary": (
            "NVC is described as a governance and yield-boosting token. "
            "Fee-sharing mechanics are referenced but not formally specified. "
            "Vesting schedule disclosed at high level only — no formal tokenomics model published."
        ),
        "extracted_metadata": {
            "founded": "2023",
            "team_disclosed": "partial",
            "audits_count": "1 (self-reported, report not public)",
        },
        "sources": [
            {"source_type": "website", "url": "https://novacash.fi", "status": "simulated", "raw_excerpt": "NovaCash Finance — Yield for emerging markets. The future of DeFi is borderless.", "full_text_length": 2800, "fetch_error": None},
            {"source_type": "whitepaper", "url": None, "status": "skipped", "raw_excerpt": None, "full_text_length": 0, "fetch_error": "No whitepaper URL provided"},
            {"source_type": "github", "url": "https://github.com/novacash-fi", "status": "simulated", "raw_excerpt": None, "full_text_length": 0, "fetch_error": None},
            {"source_type": "docs", "url": "https://docs.novacash.fi", "status": "simulated", "raw_excerpt": "NovaCash docs. Staking: deposit NVC tokens to earn protocol fees.", "full_text_length": 3100, "fetch_error": None},
        ],
        "missing_sources": ["whitepaper"],
        "source_coverage_pct": 62.5,
        "github_signals": {
            "repo_url": "https://github.com/novacash-fi/contracts",
            "stars": 89,
            "forks": 12,
            "open_issues": 7,
            "last_commit_date": "2025-09-10",
            "contributor_count": 4,
            "language": "Solidity",
            "is_active": True,
            "signal_strength": "moderate",
            "notes": ["Fewer than 5 contributors — possible small team risk"],
        },
        "red_flags": [
            {"category": "Team Transparency", "description": "5 of 7 team members identified only by pseudonym", "severity": "medium", "source_reference": "website"},
            {"category": "Documentation", "description": "No public whitepaper — only a litepaper with limited technical depth", "severity": "medium", "source_reference": "docs"},
            {"category": "Audit", "description": "Audit claimed but public report not linked", "severity": "medium", "source_reference": "website"},
            {"category": "Tokenomics", "description": "Vesting schedule mentioned but no formal model or cliff dates provided", "severity": "low", "source_reference": "docs"},
        ],
        "credibility_indicators": [
            "Two founders named with verifiable LinkedIn",
            "Active GitHub with recent Solidity commits",
            "Functional product demo available on testnet",
        ],
        "scoring": {
            "team_transparency": {"name": "Team Transparency", "score": 9, "max_score": 20, "rationale": "Only partial team disclosed. Anonymous contributors raise concerns.", "evidence_snippets": ["5 of 7 team members pseudonymous"]},
            "documentation_quality": {"name": "Documentation Quality", "score": 7, "max_score": 15, "rationale": "Litepaper exists but lacks depth. No full whitepaper.", "evidence_snippets": ["Litepaper: 2,100 words, no formal economic model"]},
            "token_utility_clarity": {"name": "Token Utility Clarity", "score": 8, "max_score": 15, "rationale": "Governance + fee-share described at high level. Mechanics not formally specified.", "evidence_snippets": []},
            "github_engineering_signal": {"name": "GitHub / Engineering Signal", "score": 8, "max_score": 15, "rationale": "Moderate GitHub activity. Low contributor count is a concern.", "evidence_snippets": ["4 contributors", "Last commit Sep 10"]},
            "ecosystem_credibility": {"name": "Ecosystem Credibility", "score": 5, "max_score": 10, "rationale": "Testnet product exists. No mainnet TVL data available.", "evidence_snippets": []},
            "research_completeness": {"name": "Research Completeness", "score": 6, "max_score": 10, "rationale": "3 of 4 source types available. Whitepaper missing.", "evidence_snippets": []},
            "hype_penalty": {"name": "Hype / Inconsistency Penalty", "score": -5, "max_score": 0, "rationale": "Website uses 'revolutionary', 'game-changing' language without supporting evidence.", "evidence_snippets": ["'The future of DeFi is borderless and limitless' — unsubstantiated"]},
            "total_score": 38,
            "risk_level": "medium",
            "recommendation": "Monitor — Needs More Data",
            "score_breakdown_pct": 44.7,
        },
        "executive_summary": (
            "NovaCash Finance presents a medium-risk profile. "
            "Positive signals include active GitHub development and partial team disclosure. "
            "Concerns include anonymous team members, absence of a public whitepaper, "
            "an unverifiable audit claim, and vague tokenomics. "
            "Recommend requesting full team disclosure, public audit report, and formal whitepaper before proceeding."
        ),
        "analyst_notes": "Put on watch list. Request full team KYC and public audit before next review.",
        "missing_information": ["Full whitepaper not published", "Audit report not public", "Full team identities not disclosed", "Tokenomics cliff dates unconfirmed"],
        "agent_steps_log": ["[DEMO] Intake validated", "[DEMO] Research complete (whitepaper missing)", "[DEMO] GitHub fetched", "[DEMO] Scoring complete", "[DEMO] Memo written"],
        "is_demo": True,
        "demo_scenario": "medium",
    },

    "high_risk": {
        "report_id": "demo-highrisk-001",
        "created_at": "2025-10-01T11:00:00",
        "project_name": "MoonShard AI (DEMO)",
        "token_ticker": "MSHA",
        "project_summary": (
            "MoonShard AI claims to be an 'AI-powered blockchain that auto-optimizes "
            "cross-chain liquidity using quantum-inspired algorithms.' "
            "No named team members are disclosed. Website is a single landing page "
            "with no documentation link. No GitHub repository was found. "
            "Whitepaper URL leads to a 3-page PDF with no technical specification. "
            "Roadmap consists of vague quarterly milestones with no deliverables."
        ),
        "token_utility_summary": (
            "MSHA is described as the 'fuel of the ecosystem' with 10,000x potential claimed in "
            "promotional material. No formal utility definition, governance structure, "
            "fee mechanism, or vesting schedule is provided anywhere."
        ),
        "extracted_metadata": {
            "team_disclosed": "none",
            "audits_count": "0",
            "documentation": "minimal",
        },
        "sources": [
            {"source_type": "website", "url": "https://moonshard.ai", "status": "simulated", "raw_excerpt": "MoonShard AI — The quantum AI blockchain. 10x, 100x, 1000x? Join the revolution. Limited presale slots.", "full_text_length": 800, "fetch_error": None},
            {"source_type": "whitepaper", "url": "https://moonshard.ai/wp.pdf", "status": "simulated", "raw_excerpt": "MoonShard AI Whitepaper v0.1. Our vision is to build the most advanced AI blockchain. Tokenomics TBD.", "full_text_length": 1100, "fetch_error": None},
            {"source_type": "github", "url": None, "status": "skipped", "raw_excerpt": None, "full_text_length": 0, "fetch_error": "No GitHub URL provided"},
            {"source_type": "docs", "url": None, "status": "skipped", "raw_excerpt": None, "full_text_length": 0, "fetch_error": "No docs URL provided"},
        ],
        "missing_sources": ["github", "docs", "team_page"],
        "source_coverage_pct": 25.0,
        "github_signals": None,
        "red_flags": [
            {"category": "Team Anonymity", "description": "No team members disclosed anywhere — complete anonymity", "severity": "high", "source_reference": "website"},
            {"category": "False Technical Claims", "description": "Claims 'quantum-inspired algorithms' and 'AI optimization' with zero technical specification", "severity": "high", "source_reference": "whitepaper"},
            {"category": "Hype Language", "description": "Website uses '10x, 100x, 1000x potential' — hallmark of speculative promotion", "severity": "high", "source_reference": "website"},
            {"category": "No Engineering Signal", "description": "No GitHub repository found — no verifiable code exists", "severity": "high", "source_reference": "N/A"},
            {"category": "Incomplete Documentation", "description": "3-page whitepaper with no technical depth, no tokenomics, no vesting — 'Tokenomics TBD'", "severity": "high", "source_reference": "whitepaper"},
            {"category": "Presale Urgency", "description": "'Limited presale slots' — manufactured urgency with no legal framework", "severity": "high", "source_reference": "website"},
            {"category": "No Audit", "description": "No security audit performed or referenced", "severity": "high", "source_reference": "N/A"},
        ],
        "credibility_indicators": [],
        "scoring": {
            "team_transparency": {"name": "Team Transparency", "score": 0, "max_score": 20, "rationale": "Zero team disclosure. Complete anonymity.", "evidence_snippets": ["No team page found", "No LinkedIn or social profiles linked"]},
            "documentation_quality": {"name": "Documentation Quality", "score": 1, "max_score": 15, "rationale": "3-page 'whitepaper' with no technical content. No docs site.", "evidence_snippets": ["'Tokenomics TBD' in whitepaper"]},
            "token_utility_clarity": {"name": "Token Utility Clarity", "score": 0, "max_score": 15, "rationale": "No utility defined. '10,000x potential' is not a utility.", "evidence_snippets": ["No staking, governance, or fee mechanism described"]},
            "github_engineering_signal": {"name": "GitHub / Engineering Signal", "score": 0, "max_score": 15, "rationale": "No GitHub found. No code signal whatsoever.", "evidence_snippets": ["No repository URL provided or discoverable"]},
            "ecosystem_credibility": {"name": "Ecosystem Credibility", "score": 0, "max_score": 10, "rationale": "No partnerships, no TVL, no verifiable ecosystem activity.", "evidence_snippets": []},
            "research_completeness": {"name": "Research Completeness", "score": 2, "max_score": 10, "rationale": "Only 2 of 4 source types available, both extremely sparse.", "evidence_snippets": []},
            "hype_penalty": {"name": "Hype / Inconsistency Penalty", "score": -15, "max_score": 0, "rationale": "Maximum penalty: '10,000x' claims, 'quantum AI' without spec, presale urgency tactics.", "evidence_snippets": ["'10x, 100x, 1000x? Join the revolution'", "'quantum-inspired algorithms' — zero technical backing"]},
            "total_score": -12,
            "risk_level": "high",
            "recommendation": "High Risk — Do Not List",
            "score_breakdown_pct": 0.0,
        },
        "executive_summary": (
            "MoonShard AI exhibits multiple critical high-risk indicators. "
            "The project has zero team transparency, no verifiable code, fabricated technical claims, "
            "hype-heavy marketing language, and a meaningless whitepaper. "
            "These characteristics are consistent with speculative token promotion schemes. "
            "Recommendation: Do not list. Flag for trust & safety review."
        ),
        "analyst_notes": "Forward to T&S team. Flag MSHA for potential predatory promotion review. Do not engage.",
        "missing_information": ["All team identities unknown", "No verifiable code or engineering activity", "No audit", "Tokenomics undefined", "No governance structure", "No legal disclosure"],
        "agent_steps_log": ["[DEMO] Intake validated", "[DEMO] Research returned minimal content", "[DEMO] GitHub not found", "[DEMO] High-risk scoring triggered", "[DEMO] Rejection memo written"],
        "is_demo": True,
        "demo_scenario": "high_risk",
    },
}


def get_demo_report(scenario: str) -> dict:
    """Return a pre-built demo report by scenario key."""
    return DEMO_REPORTS.get(scenario, DEMO_REPORTS["medium"])


def all_demo_reports() -> list[dict]:
    return list(DEMO_REPORTS.values())
