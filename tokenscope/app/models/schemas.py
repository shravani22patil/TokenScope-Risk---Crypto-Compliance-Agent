"""
models/schemas.py
-----------------
All Pydantic schemas for TokenScope Risk.
Used by agents, API, and storage layers.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, HttpUrl


# ── Enums ─────────────────────────────────────────────────────────────────────

class RiskLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    REVIEW = "review"
    STRONG = "strong"


class RecommendationLabel(str, Enum):
    REJECT = "High Risk — Do Not List"
    MONITOR = "Monitor — Needs More Data"
    REVIEW = "Proceed to Deeper Review"
    PROCEED = "Strong Initial Signal — Proceed"


class SourceStatus(str, Enum):
    FETCHED = "fetched"
    FAILED = "failed"
    SKIPPED = "skipped"
    SIMULATED = "simulated"


# ── Input ─────────────────────────────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=120)
    token_ticker: Optional[str] = Field(None, max_length=20)
    website_url: Optional[str] = None
    whitepaper_url: Optional[str] = None
    github_url: Optional[str] = None
    docs_url: Optional[str] = None
    extra_notes: Optional[str] = Field(None, max_length=1000)
    use_demo_data: bool = False
    demo_scenario: Optional[str] = None  # "strong" | "medium" | "high_risk"


# ── Source evidence ───────────────────────────────────────────────────────────

class SourceEvidence(BaseModel):
    source_type: str           # "website" | "whitepaper" | "github" | "docs"
    url: Optional[str] = None
    status: SourceStatus
    raw_excerpt: Optional[str] = None   # First 800 chars of extracted text
    full_text_length: int = 0
    fetch_error: Optional[str] = None


# ── GitHub signals ────────────────────────────────────────────────────────────

class GitHubSignals(BaseModel):
    repo_url: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    open_issues: Optional[int] = None
    last_commit_date: Optional[str] = None
    contributor_count: Optional[int] = None
    language: Optional[str] = None
    is_active: bool = False
    signal_strength: str = "unknown"   # "weak" | "moderate" | "strong"
    notes: list[str] = Field(default_factory=list)


# ── Risk dimensions ───────────────────────────────────────────────────────────

class RiskDimension(BaseModel):
    name: str
    score: int
    max_score: int
    rationale: str
    evidence_snippets: list[str] = Field(default_factory=list)


class RedFlag(BaseModel):
    category: str
    description: str
    severity: str   # "low" | "medium" | "high"
    source_reference: Optional[str] = None


# ── Scoring ───────────────────────────────────────────────────────────────────

class ScoringResult(BaseModel):
    team_transparency: RiskDimension
    documentation_quality: RiskDimension
    token_utility_clarity: RiskDimension
    github_engineering_signal: RiskDimension
    ecosystem_credibility: RiskDimension
    research_completeness: RiskDimension
    hype_penalty: RiskDimension

    total_score: int
    risk_level: RiskLevel
    recommendation: RecommendationLabel
    score_breakdown_pct: float   # total / max_possible


# ── Full report ───────────────────────────────────────────────────────────────

class DueDiligenceReport(BaseModel):
    report_id: str
    created_at: datetime
    project_name: str
    token_ticker: Optional[str] = None

    # Project profile
    project_summary: str
    token_utility_summary: str
    extracted_metadata: dict[str, Any] = Field(default_factory=dict)

    # Sources
    sources: list[SourceEvidence] = Field(default_factory=list)
    missing_sources: list[str] = Field(default_factory=list)
    source_coverage_pct: float = 0.0

    # Signals
    github_signals: Optional[GitHubSignals] = None

    # Risk
    red_flags: list[RedFlag] = Field(default_factory=list)
    credibility_indicators: list[str] = Field(default_factory=list)
    scoring: ScoringResult

    # Memo
    executive_summary: str
    analyst_notes: str
    missing_information: list[str] = Field(default_factory=list)

    # Meta
    agent_steps_log: list[str] = Field(default_factory=list)
    is_demo: bool = False
    demo_scenario: Optional[str] = None


# ── Storage ───────────────────────────────────────────────────────────────────

class ReportListItem(BaseModel):
    report_id: str
    project_name: str
    token_ticker: Optional[str]
    risk_level: RiskLevel
    total_score: int
    recommendation: RecommendationLabel
    created_at: datetime
    is_demo: bool
