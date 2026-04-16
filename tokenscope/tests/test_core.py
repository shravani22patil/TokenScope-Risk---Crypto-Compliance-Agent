"""
tests/test_core.py
------------------
Basic test suite for TokenScope Risk core components.
Run: pytest tests/ -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# ── Schema tests ──────────────────────────────────────────────────────────────

def test_analysis_request_valid():
    from app.models.schemas import AnalysisRequest
    req = AnalysisRequest(project_name="Test Token", token_ticker="TST")
    assert req.project_name == "Test Token"
    assert req.token_ticker == "TST"


def test_analysis_request_no_ticker():
    from app.models.schemas import AnalysisRequest
    req = AnalysisRequest(project_name="No Ticker Project")
    assert req.token_ticker is None


def test_analysis_request_empty_name_fails():
    from app.models.schemas import AnalysisRequest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        AnalysisRequest(project_name="")


# ── Demo data tests ───────────────────────────────────────────────────────────

def test_demo_strong_exists():
    from app.data.demo_data import get_demo_report
    demo = get_demo_report("strong")
    assert demo["project_name"] == "Helios Protocol (DEMO)"
    assert demo["scoring"]["total_score"] == 76
    assert demo["scoring"]["risk_level"] == "strong"


def test_demo_medium_exists():
    from app.data.demo_data import get_demo_report
    demo = get_demo_report("medium")
    assert demo["scoring"]["risk_level"] == "medium"
    assert len(demo["red_flags"]) > 0


def test_demo_high_risk_exists():
    from app.data.demo_data import get_demo_report
    demo = get_demo_report("high_risk")
    assert demo["scoring"]["risk_level"] == "high"
    assert demo["scoring"]["recommendation"] == "High Risk — Do Not List"


def test_all_demos_loadable():
    from app.data.demo_data import all_demo_reports
    demos = all_demo_reports()
    assert len(demos) == 3


# ── Database tests ────────────────────────────────────────────────────────────

def test_db_init_and_save(tmp_path):
    os.environ["DATABASE_URL"] = str(tmp_path / "test.db")
    from importlib import reload
    import app.services.database as db
    reload(db)
    db.init_db()

    from app.data.demo_data import get_demo_report
    demo = get_demo_report("strong")
    db.save_report(demo)

    fetched = db.get_report("demo-strong-001")
    assert fetched is not None
    assert fetched["project_name"] == "Helios Protocol (DEMO)"


def test_db_list_reports(tmp_path):
    os.environ["DATABASE_URL"] = str(tmp_path / "test2.db")
    from importlib import reload
    import app.services.database as db
    reload(db)
    db.init_db()

    from app.data.demo_data import all_demo_reports
    for d in all_demo_reports():
        db.save_report(d)

    reports = db.list_reports()
    assert len(reports) == 3


# ── Exporter tests ────────────────────────────────────────────────────────────

def test_markdown_memo_generated():
    from app.services.exporter import generate_markdown_memo
    from app.data.demo_data import get_demo_report
    memo = generate_markdown_memo(get_demo_report("strong"))
    assert "# TokenScope Risk" in memo
    assert "Helios Protocol" in memo
    assert "Executive Summary" in memo
    assert len(memo) > 500


def test_markdown_memo_high_risk():
    from app.services.exporter import generate_markdown_memo
    from app.data.demo_data import get_demo_report
    memo = generate_markdown_memo(get_demo_report("high_risk"))
    assert "HIGH RISK" in memo.upper() or "Do Not List" in memo


# ── Scraper utility tests ─────────────────────────────────────────────────────

def test_signal_strength_strong():
    from app.services.scraper import _signal_strength
    assert _signal_strength(1500, 300, 40, True) == "strong"


def test_signal_strength_weak():
    from app.services.scraper import _signal_strength
    assert _signal_strength(5, 1, 1, False) == "weak"


def test_is_active_old_date():
    from app.services.scraper import _is_active
    assert _is_active("2020-01-01") is False


def test_github_fallback_format():
    from app.services.scraper import _github_fallback
    fb = _github_fallback("test error")
    assert fb["signal_strength"] == "unknown"
    assert "test error" in fb["notes"][0]


def test_clean_text():
    from app.services.scraper import _clean
    messy = "hello   \n\n\n\n   world   \n"
    cleaned = _clean(messy)
    assert "hello" in cleaned
    assert "world" in cleaned


# ── Agent pipeline structure tests ───────────────────────────────────────────

def test_intake_agent_detects_missing():
    from app.agents.orchestrator import AgentState, intake_agent
    from app.models.schemas import AnalysisRequest
    req = AnalysisRequest(project_name="Test")
    state = AgentState(req)
    state = intake_agent(state)
    assert len(state.missing_information) == 4  # all 4 sources missing


def test_intake_agent_with_urls():
    from app.agents.orchestrator import AgentState, intake_agent
    from app.models.schemas import AnalysisRequest
    req = AnalysisRequest(
        project_name="Test",
        website_url="https://example.com",
        github_url="https://github.com/test/repo",
    )
    state = AgentState(req)
    state = intake_agent(state)
    # Only whitepaper and docs should be missing
    assert "website_url" not in state.missing_information
    assert "GitHub repository URL" not in state.missing_information


def test_state_source_coverage_zero():
    from app.agents.orchestrator import AgentState
    from app.models.schemas import AnalysisRequest
    state = AgentState(AnalysisRequest(project_name="X"))
    assert state.source_coverage_pct() == 0.0


def test_state_source_coverage_partial():
    from app.agents.orchestrator import AgentState
    from app.models.schemas import AnalysisRequest
    state = AgentState(AnalysisRequest(project_name="X"))
    state.sources = [
        {"source_type": "website", "status": "fetched"},
        {"source_type": "docs", "status": "fetched"},
        {"source_type": "whitepaper", "status": "skipped"},
        {"source_type": "github", "status": "failed"},
    ]
    assert state.source_coverage_pct() == 50.0


# ── FastAPI endpoint tests ────────────────────────────────────────────────────

def test_api_health():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_api_reports_list():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    resp = client.get("/reports")
    assert resp.status_code == 200
    assert "reports" in resp.json()


def test_api_demo_analyze():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    resp = client.post("/analyze", json={
        "project_name": "Test",
        "use_demo_data": True,
        "demo_scenario": "strong",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "complete"
    assert data["report"]["scoring"]["risk_level"] == "strong"


def test_api_report_not_found():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    resp = client.get("/report/nonexistent-id-xyz")
    assert resp.status_code == 404


def test_api_export_memo():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    resp = client.post("/export/demo-strong-001")
    assert resp.status_code == 200
    assert "TokenScope Risk" in resp.text
