"""
streamlit_app.py
----------------
TokenScope Risk — Main Streamlit dashboard.
Premium compliance intelligence UI for crypto listings teams.

Run: streamlit run streamlit_app.py
"""

import json
import os
import sys
import time
from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

# Allow imports from project root
sys.path.insert(0, os.path.dirname(__file__))

from app.data.demo_data import get_demo_report, all_demo_reports
from app.services.database import init_db, save_report, list_reports, get_report
from app.services.exporter import generate_markdown_memo

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TokenScope Risk",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize DB ─────────────────────────────────────────────────────────────
init_db()

# ── Load demo data into DB on first run ──────────────────────────────────────
if "demos_loaded" not in st.session_state:
    for demo in all_demo_reports():
        save_report(demo)
    st.session_state.demos_loaded = True

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #0c0e12; color: #d4d8e2; }
.stApp { background: #0c0e12; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1117 !important;
    border-right: 1px solid #1e2330;
}
[data-testid="stSidebar"] * { color: #d4d8e2 !important; }

/* ── Typography ── */
h1, h2, h3 { font-family: 'Instrument Serif', serif !important; letter-spacing: -0.02em; }
.mono { font-family: 'IBM Plex Mono', monospace; font-size: 12px; }

/* ── Containers ── */
.block-container { padding: 2rem 2.5rem; max-width: 1300px; }
[data-testid="stVerticalBlock"] { gap: 0.5rem; }

/* ── Cards ── */
.ts-card {
    background: #141720;
    border: 1px solid #1e2330;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.ts-card:hover { border-color: #2a3350; }

.ts-kpi {
    background: #141720;
    border: 1px solid #1e2330;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
}

/* ── Risk badges ── */
.badge-high    { background: rgba(239,68,68,0.12); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.badge-medium  { background: rgba(245,158,11,0.12); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.badge-review  { background: rgba(34,197,94,0.12); color: #22c55e; border: 1px solid rgba(34,197,94,0.3); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.badge-strong  { background: rgba(59,130,246,0.12); color: #3b82f6; border: 1px solid rgba(59,130,246,0.3); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }

/* ── Red flag cards ── */
.flag-high   { border-left: 3px solid #ef4444; background: rgba(239,68,68,0.05); padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 6px 0; }
.flag-medium { border-left: 3px solid #f59e0b; background: rgba(245,158,11,0.05); padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 6px 0; }
.flag-low    { border-left: 3px solid #64748b; background: rgba(100,116,139,0.05); padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 6px 0; }

/* ── Source chips ── */
.src-ok   { background: rgba(34,197,94,0.1);   color: #22c55e; padding: 3px 10px; border-radius: 20px; font-size: 11px; display: inline-block; margin: 3px; }
.src-fail { background: rgba(239,68,68,0.1);   color: #ef4444; padding: 3px 10px; border-radius: 20px; font-size: 11px; display: inline-block; margin: 3px; }
.src-skip { background: rgba(100,116,139,0.1); color: #94a3b8; padding: 3px 10px; border-radius: 20px; font-size: 11px; display: inline-block; margin: 3px; }
.src-demo { background: rgba(59,130,246,0.1);  color: #60a5fa; padding: 3px 10px; border-radius: 20px; font-size: 11px; display: inline-block; margin: 3px; }

/* ── Logo area ── */
.ts-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 500;
    color: #e2e8f0;
    letter-spacing: 0.05em;
}
.ts-logo-accent { color: #3b82f6; }

/* ── Progress bar ── */
.stProgress > div > div { background: #3b82f6; }

/* ── Input ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #141720 !important;
    border: 1px solid #1e2330 !important;
    color: #d4d8e2 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #1e3a8a;
    color: #e2e8f0;
    border: 1px solid #2563eb;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.01em;
    transition: all 0.2s;
}
.stButton > button:hover { background: #1d4ed8; border-color: #3b82f6; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] { font-family: 'DM Sans', sans-serif; color: #64748b; font-size: 14px; }
.stTabs [aria-selected="true"] { color: #e2e8f0; }
.stTabs [data-baseweb="tab-border"] { background: #3b82f6 !important; }
.stTabs [data-baseweb="tab-highlight"] { background: #3b82f6 !important; }

/* ── Misc ── */
#MainMenu, footer { visibility: hidden; }
.stAlert { border-radius: 8px; }
[data-testid="stExpander"] { background: #141720; border: 1px solid #1e2330; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

RISK_BADGE = {
    "high":   '<span class="badge-high">🔴 HIGH RISK</span>',
    "medium": '<span class="badge-medium">🟡 MEDIUM RISK</span>',
    "review": '<span class="badge-review">🟢 REVIEW FURTHER</span>',
    "strong": '<span class="badge-strong">✅ STRONG SIGNAL</span>',
}
RISK_COLOR = {"high": "#ef4444", "medium": "#f59e0b", "review": "#22c55e", "strong": "#3b82f6"}
SEV_CLASS = {"high": "flag-high", "medium": "flag-medium", "low": "flag-low"}
SRC_CLASS = {"fetched": "src-ok", "failed": "src-fail", "skipped": "src-skip", "simulated": "src-demo"}
SRC_LABEL = {"fetched": "✓ fetched", "failed": "✗ failed", "skipped": "— skipped", "simulated": "◆ demo"}


def risk_gauge(score: int, max_score: int = 85) -> go.Figure:
    pct = max(0, min(100, score / max_score * 100))
    color = "#ef4444" if pct < 35 else "#f59e0b" if pct < 65 else "#22c55e" if pct < 88 else "#3b82f6"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        number={"font": {"color": color, "size": 36, "family": "IBM Plex Mono"}, "suffix": f"/{max_score}"},
        gauge={
            "axis": {"range": [0, max_score], "tickcolor": "#374151", "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#1e2330",
            "bordercolor": "#1e2330",
            "steps": [
                {"range": [0, 30], "color": "rgba(239,68,68,0.08)"},
                {"range": [30, 55], "color": "rgba(245,158,11,0.08)"},
                {"range": [55, 75], "color": "rgba(34,197,94,0.08)"},
                {"range": [75, 85], "color": "rgba(59,130,246,0.08)"},
            ],
        },
    ))
    fig.update_layout(
        height=220, margin=dict(l=20, r=20, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#d4d8e2",
    )
    return fig


def dimension_radar(scoring: dict) -> go.Figure:
    dims = [
        ("team_transparency", "Team"),
        ("documentation_quality", "Docs"),
        ("token_utility_clarity", "Utility"),
        ("github_engineering_signal", "GitHub"),
        ("ecosystem_credibility", "Ecosystem"),
        ("research_completeness", "Coverage"),
    ]
    vals, labels, maxes = [], [], []
    for key, label in dims:
        d = scoring.get(key, {})
        sc = max(0, d.get("score", 0))
        mx = d.get("max_score", 1)
        vals.append(sc / mx * 100)
        labels.append(label)
        maxes.append(mx)

    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=labels + [labels[0]],
        fill="toself",
        fillcolor="rgba(59,130,246,0.12)",
        line=dict(color="#3b82f6", width=2),
        marker=dict(size=5, color="#3b82f6"),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], tickcolor="#374151", gridcolor="#1e2330", linecolor="#1e2330", tickfont=dict(color="#64748b", size=10)),
            angularaxis=dict(tickcolor="#374151", gridcolor="#1e2330", linecolor="#1e2330", tickfont=dict(color="#94a3b8", size=11)),
        ),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#d4d8e2",
        height=300, margin=dict(l=30, r=30, t=20, b=20),
        showlegend=False,
    )
    return fig


def dimension_bars(scoring: dict) -> go.Figure:
    dims = [
        ("team_transparency", "Team Transparency", 20),
        ("documentation_quality", "Documentation", 15),
        ("token_utility_clarity", "Token Utility", 15),
        ("github_engineering_signal", "GitHub Signal", 15),
        ("ecosystem_credibility", "Ecosystem", 10),
        ("research_completeness", "Coverage", 10),
    ]
    labels, vals, maxes, colors = [], [], [], []
    for key, label, mx in dims:
        sc = max(0, scoring.get(key, {}).get("score", 0))
        pct = sc / mx
        labels.append(label)
        vals.append(sc)
        maxes.append(mx)
        colors.append("#ef4444" if pct < 0.35 else "#f59e0b" if pct < 0.65 else "#3b82f6")

    fig = go.Figure()
    fig.add_bar(
        y=labels, x=maxes, orientation="h",
        marker_color="rgba(30,35,48,0.8)", name="Max",
        hoverinfo="skip",
    )
    fig.add_bar(
        y=labels, x=vals, orientation="h",
        marker_color=colors, name="Score",
        text=[f"{v}/{m}" for v, m in zip(vals, maxes)],
        textfont=dict(color="#d4d8e2", size=11, family="IBM Plex Mono"),
        textposition="inside",
    )
    fig.update_layout(
        barmode="overlay", height=260,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#d4d8e2",
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )
    return fig


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 24px; border-bottom:1px solid #1e2330; margin-bottom:20px;">
      <div class="ts-logo">TOKEN<span class="ts-logo-accent">SCOPE</span> RISK</div>
      <div style="color:#475569;font-size:11px;margin-top:4px;font-family:'IBM Plex Mono',monospace;">v1.0 · Compliance Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🔍 New Analysis", "📋 Report History", "📖 How It Works"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent reports in sidebar
    recent = list_reports(limit=5)
    if recent:
        st.markdown("<div style='color:#475569;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>Recent Analyses</div>", unsafe_allow_html=True)
        for r in recent:
            risk = r["risk_level"]
            icon = {"high": "🔴", "medium": "🟡", "review": "🟢", "strong": "✅"}.get(risk, "⬜")
            demo_tag = " [DEMO]" if r["is_demo"] else ""
            if st.button(f"{icon} {r['project_name'][:22]}{demo_tag}", key=f"sb_{r['report_id']}", use_container_width=True):
                st.session_state["view_report_id"] = r["report_id"]
                st.session_state["page_override"] = "view_report"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px;color:#374151;border-top:1px solid #1e2330;padding-top:16px;">
    For internal decision-support only.<br>Not financial or legal advice.
    </div>
    """, unsafe_allow_html=True)


# ── Page override (for sidebar navigation to a report) ────────────────────────
if "page_override" in st.session_state and st.session_state["page_override"] == "view_report":
    page = "view_report"
    if st.button("← Back", key="back_btn"):
        del st.session_state["page_override"]
        del st.session_state["view_report_id"]
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: New Analysis
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🔍 New Analysis":
    st.markdown("## Due-Diligence Analysis")
    st.markdown("<p style='color:#64748b;margin-top:-12px;'>Submit a token or project for multi-step AI compliance review</p>", unsafe_allow_html=True)

    # Demo buttons
    st.markdown("**Quick Demo:**")
    dc1, dc2, dc3, dc4 = st.columns(4)
    with dc1:
        if st.button("✅ Strong Signal Demo", use_container_width=True):
            st.session_state["demo_result"] = get_demo_report("strong")
            st.rerun()
    with dc2:
        if st.button("🟡 Medium Risk Demo", use_container_width=True):
            st.session_state["demo_result"] = get_demo_report("medium")
            st.rerun()
    with dc3:
        if st.button("🔴 High Risk Demo", use_container_width=True):
            st.session_state["demo_result"] = get_demo_report("high_risk")
            st.rerun()
    with dc4:
        if st.button("🗂 View All Reports", use_container_width=True):
            st.session_state["page_override"] = None
            st.rerun()

    st.markdown("---")

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("analysis_form"):
        st.markdown("### Project Details")
        col1, col2 = st.columns([2, 1])
        with col1:
            project_name = st.text_input("Project / Token Name *", placeholder="e.g. Helios Protocol")
        with col2:
            token_ticker = st.text_input("Ticker Symbol", placeholder="e.g. HLS")

        st.markdown("### Source Links")
        col3, col4 = st.columns(2)
        with col3:
            website_url = st.text_input("Official Website", placeholder="https://project.io")
            whitepaper_url = st.text_input("Whitepaper / Litepaper URL", placeholder="https://project.io/whitepaper.pdf")
        with col4:
            github_url = st.text_input("GitHub Repository", placeholder="https://github.com/org/repo")
            docs_url = st.text_input("Documentation Site", placeholder="https://docs.project.io")

        extra_notes = st.text_area("Analyst Notes (optional)", placeholder="Any context, concerns, or background information...", height=80)

        submitted = st.form_submit_button("🔍 Run Analysis", use_container_width=True)

    if submitted and project_name:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            st.error("⚠️ ANTHROPIC_API_KEY not set. Add it to your .env file. Use demo mode instead.")
        else:
            # Run pipeline
            from app.models.schemas import AnalysisRequest
            from app.agents.orchestrator import run_analysis

            req = AnalysisRequest(
                project_name=project_name,
                token_ticker=token_ticker or None,
                website_url=website_url or None,
                whitepaper_url=whitepaper_url or None,
                github_url=github_url or None,
                docs_url=docs_url or None,
                extra_notes=extra_notes or None,
            )

            progress_container = st.container()
            status_box = progress_container.empty()
            step_log = []

            def update_progress(msg: str):
                step_log.append(msg)
                status_box.markdown(
                    f"<div class='ts-card'><div style='color:#64748b;font-size:11px;font-family:IBM Plex Mono,monospace;'>AGENT PIPELINE RUNNING</div>"
                    + "".join(f"<div style='font-size:12px;color:#94a3b8;margin-top:4px;'>→ {s}</div>" for s in step_log[-5:])
                    + "</div>",
                    unsafe_allow_html=True,
                )

            with st.spinner("Running compliance analysis..."):
                try:
                    result = run_analysis(req, progress_cb=update_progress)
                    save_report(result)
                    status_box.empty()
                    st.session_state["demo_result"] = result
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    elif submitted and not project_name:
        st.warning("Project name is required.")


# ── Report display (shared by demo result and history view) ───────────────────
def render_report(report: dict):
    scoring = report.get("scoring", {})
    risk = scoring.get("risk_level", "unknown")
    total = scoring.get("total_score", 0)
    rec = scoring.get("recommendation", "—")

    # ── Header ────────────────────────────────────────────────────────────────
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"## {report.get('project_name', '—')}")
        ticker = report.get("token_ticker")
        created = report.get("created_at", "")[:10]
        meta_parts = []
        if ticker: meta_parts.append(f"**{ticker}**")
        meta_parts.append(f"Analyzed {created}")
        if report.get("is_demo"): meta_parts.append("🔵 DEMO DATA")
        st.markdown("<span style='color:#64748b;'>" + " · ".join(meta_parts) + "</span>", unsafe_allow_html=True)
        st.markdown(RISK_BADGE.get(risk, ""), unsafe_allow_html=True)
        st.markdown(f"<p style='color:#94a3b8;margin-top:8px;font-size:14px;'>{rec}</p>", unsafe_allow_html=True)
    with col_h2:
        st.plotly_chart(risk_gauge(max(0, total)), use_container_width=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tabs = st.tabs(["📊 Overview", "⚠️ Risk Analysis", "🔬 Engineering", "📂 Evidence", "📄 Export Memo"])

    # ── TAB 1: Overview ───────────────────────────────────────────────────────
    with tabs[0]:
        # KPI row
        kc1, kc2, kc3, kc4 = st.columns(4)
        kpis = [
            ("Risk Score", f"{max(0, total)}/85", RISK_COLOR.get(risk, "#94a3b8")),
            ("Sources Analyzed", f"{sum(1 for s in report.get('sources',[]) if s.get('status') in ('fetched','simulated'))}/4", "#94a3b8"),
            ("Red Flags", str(len(report.get("red_flags", []))), "#ef4444" if report.get("red_flags") else "#22c55e"),
            ("Coverage", f"{report.get('source_coverage_pct', 0):.0f}%", "#94a3b8"),
        ]
        for col, (label, val, color) in zip([kc1, kc2, kc3, kc4], kpis):
            with col:
                st.markdown(f"""<div class="ts-kpi">
                    <div style="color:#475569;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
                    <div style="color:{color};font-size:26px;font-weight:700;font-family:IBM Plex Mono,monospace;margin-top:6px;">{val}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_sum, col_radar = st.columns([3, 2])

        with col_sum:
            st.markdown("**Executive Summary**")
            st.markdown(f"<div class='ts-card'>{report.get('executive_summary', '—')}</div>", unsafe_allow_html=True)
            st.markdown("**Project Summary**")
            st.markdown(f"<div class='ts-card'>{report.get('project_summary', '—')}</div>", unsafe_allow_html=True)
            st.markdown("**Token Utility**")
            st.markdown(f"<div class='ts-card'>{report.get('token_utility_summary', '—')}</div>", unsafe_allow_html=True)

        with col_radar:
            st.markdown("**Score Dimensions**")
            st.plotly_chart(dimension_radar(scoring), use_container_width=True)

        # Source coverage
        st.markdown("**Source Coverage**")
        src_html = ""
        for src in report.get("sources", []):
            st_key = src.get("status", "skipped")
            cls = SRC_CLASS.get(st_key, "src-skip")
            lbl = SRC_LABEL.get(st_key, "—")
            src_html += f'<span class="{cls}">{src.get("source_type","?")} {lbl}</span>'
        st.markdown(src_html or "_No sources_", unsafe_allow_html=True)

        missing = report.get("missing_sources", []) or report.get("missing_information", [])
        if missing:
            st.markdown("<div style='color:#64748b;font-size:12px;margin-top:8px;'>Missing: " + ", ".join(missing[:6]) + "</div>", unsafe_allow_html=True)

        # Credibility indicators
        creds = report.get("credibility_indicators", [])
        if creds:
            st.markdown("<br>**✓ Credibility Indicators**")
            for c in creds:
                st.markdown(f"<div style='color:#22c55e;font-size:13px;margin:3px 0;'>✓ {c}</div>", unsafe_allow_html=True)

    # ── TAB 2: Risk Analysis ──────────────────────────────────────────────────
    with tabs[1]:
        col_bars, col_flags = st.columns([2, 3])

        with col_bars:
            st.markdown("**Score Breakdown**")
            st.plotly_chart(dimension_bars(scoring), use_container_width=True)

            # Hype penalty
            hp = scoring.get("hype_penalty", {})
            hp_score = hp.get("score", 0)
            if hp_score < 0:
                st.markdown(f"""<div class="flag-high">
                    <div style="font-size:12px;font-weight:600;color:#ef4444;">Hype Penalty: {hp_score}</div>
                    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">{hp.get('rationale','')}</div>
                </div>""", unsafe_allow_html=True)

        with col_flags:
            flags = report.get("red_flags", [])
            st.markdown(f"**Red Flags ({len(flags)})**")
            if flags:
                for flag in flags:
                    sev = flag.get("severity", "low")
                    icon = {"high": "🚨", "medium": "⚠️", "low": "ℹ️"}.get(sev, "ℹ️")
                    cls = SEV_CLASS.get(sev, "flag-low")
                    src_ref = flag.get("source_reference", "")
                    st.markdown(f"""<div class="{cls}">
                        <div style="font-size:12px;font-weight:600;color:#d4d8e2;">{icon} [{flag.get('category','?')}] — <span style='color:#94a3b8;font-weight:400;font-size:11px;'>{sev.upper()}</span></div>
                        <div style="font-size:13px;color:#94a3b8;margin-top:4px;">{flag.get('description','')}</div>
                        {f'<div style="font-size:10px;color:#475569;margin-top:4px;font-family:IBM Plex Mono,monospace;">source: {src_ref}</div>' if src_ref else ''}
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("<div class='ts-card' style='color:#22c55e;'>✓ No red flags identified.</div>", unsafe_allow_html=True)

        # Dimension rationales
        st.markdown("<br>**Dimension Rationales**")
        dim_keys = [
            ("team_transparency", "Team Transparency"),
            ("documentation_quality", "Documentation Quality"),
            ("token_utility_clarity", "Token Utility Clarity"),
            ("github_engineering_signal", "GitHub / Engineering Signal"),
            ("ecosystem_credibility", "Ecosystem Credibility"),
            ("research_completeness", "Research Completeness"),
        ]
        for key, label in dim_keys:
            d = scoring.get(key, {})
            sc = d.get("score", 0)
            mx = d.get("max_score", 1)
            pct = max(0, sc) / mx
            bar_color = "#ef4444" if pct < 0.35 else "#f59e0b" if pct < 0.65 else "#3b82f6"
            with st.expander(f"{label} — {sc}/{mx}"):
                st.markdown(f"<div style='color:#94a3b8;font-size:13px;'>{d.get('rationale','—')}</div>", unsafe_allow_html=True)
                evs = d.get("evidence_snippets", [])
                for ev in evs:
                    st.markdown(f"<div style='color:#64748b;font-size:12px;font-family:IBM Plex Mono,monospace;margin-top:6px;padding:6px 10px;background:#0c0e12;border-radius:6px;'>{ev}</div>", unsafe_allow_html=True)

    # ── TAB 3: Engineering ────────────────────────────────────────────────────
    with tabs[2]:
        gh = report.get("github_signals")
        if not gh:
            st.markdown("<div class='ts-card' style='color:#94a3b8;'>No GitHub repository provided for this analysis.</div>", unsafe_allow_html=True)
        else:
            strength = gh.get("signal_strength", "unknown")
            s_color = {"strong": "#3b82f6", "moderate": "#f59e0b", "weak": "#ef4444", "unknown": "#64748b"}.get(strength, "#64748b")

            gc1, gc2, gc3, gc4 = st.columns(4)
            gh_kpis = [
                ("Stars", str(gh.get("stars") or "—"), "#f59e0b"),
                ("Forks", str(gh.get("forks") or "—"), "#94a3b8"),
                ("Contributors", str(gh.get("contributor_count") or "—"), "#94a3b8"),
                ("Open Issues", str(gh.get("open_issues") or "—"), "#94a3b8"),
            ]
            for col, (label, val, color) in zip([gc1, gc2, gc3, gc4], gh_kpis):
                with col:
                    st.markdown(f"""<div class="ts-kpi">
                        <div style="color:#475569;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
                        <div style="color:{color};font-size:22px;font-weight:700;font-family:IBM Plex Mono,monospace;margin-top:6px;">{val}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown(f"""<div class="ts-card">
                    <div style="color:#475569;font-size:11px;text-transform:uppercase;">Engineering Signal</div>
                    <div style="color:{s_color};font-size:20px;font-weight:700;font-family:IBM Plex Mono,monospace;margin-top:8px;">{strength.upper()}</div>
                    <div style="color:#64748b;font-size:12px;margin-top:6px;">Language: {gh.get('language') or '—'}</div>
                    <div style="color:#64748b;font-size:12px;">Last Commit: {gh.get('last_commit_date') or '—'}</div>
                    <div style="color:#64748b;font-size:12px;">Active: {'✓ Yes' if gh.get('is_active') else '✗ No (>90 days)'}</div>
                </div>""", unsafe_allow_html=True)
            with col_g2:
                notes = gh.get("notes", [])
                if notes:
                    st.markdown("<div class='ts-card'><div style='color:#475569;font-size:11px;text-transform:uppercase;'>GitHub Analyst Notes</div>", unsafe_allow_html=True)
                    for note in notes:
                        st.markdown(f"<div style='color:#f59e0b;font-size:13px;margin-top:8px;'>⚠ {note}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='ts-card' style='color:#22c55e;'>✓ No GitHub concerns.</div>", unsafe_allow_html=True)

    # ── TAB 4: Evidence ───────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("### Source Evidence Explorer")
        sources = report.get("sources", [])
        for src in sources:
            st_key = src.get("status", "skipped")
            icon = {"fetched": "✅", "failed": "❌", "skipped": "⏭️", "simulated": "🔵"}.get(st_key, "?")
            label = f"{icon} {src.get('source_type','?').upper()} — {st_key}"
            with st.expander(label):
                if src.get("url"):
                    st.markdown(f"<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#475569;'>{src['url']}</div>", unsafe_allow_html=True)
                excerpt = src.get("raw_excerpt", "")
                if excerpt:
                    st.markdown(f"<div style='background:#0c0e12;padding:12px;border-radius:8px;font-size:12px;color:#94a3b8;line-height:1.6;'>{excerpt}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color:#374151;font-size:11px;margin-top:6px;'>Full text: {src.get('full_text_length',0):,} chars extracted</div>", unsafe_allow_html=True)
                elif src.get("fetch_error"):
                    st.markdown(f"<div style='color:#ef4444;font-size:12px;'>{src['fetch_error']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color:#64748b;font-size:12px;'>No content extracted.</div>", unsafe_allow_html=True)

        # Agent log
        st.markdown("<br>**Agent Pipeline Log**")
        log = report.get("agent_steps_log", [])
        log_html = "\n".join(f"<div style='font-size:11px;color:#475569;font-family:IBM Plex Mono,monospace;'>{l}</div>" for l in log)
        st.markdown(f"<div class='ts-card'>{log_html or 'No log.'}</div>", unsafe_allow_html=True)

    # ── TAB 5: Export ─────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("### Compliance Memo Export")
        st.markdown("<p style='color:#64748b;'>Download a structured analyst memo for your listings or compliance team.</p>", unsafe_allow_html=True)

        memo_md = generate_markdown_memo(report)

        # Preview
        with st.expander("📄 Preview Memo"):
            st.markdown(memo_md)

        # Download
        st.download_button(
            label="⬇ Download Markdown Memo (.md)",
            data=memo_md,
            file_name=f"tokenscope_{report.get('project_name','report').replace(' ','_').lower()}_{report.get('report_id','')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

        st.download_button(
            label="⬇ Download Raw JSON Report",
            data=json.dumps(report, indent=2, default=str),
            file_name=f"tokenscope_{report.get('report_id','')}.json",
            mime="application/json",
            use_container_width=True,
        )

        if report.get("is_demo"):
            st.markdown("<div style='color:#60a5fa;font-size:12px;margin-top:12px;'>🔵 This is demo/simulated data for portfolio demonstration.</div>", unsafe_allow_html=True)


# Show report from session state (demo or new analysis)
if "demo_result" in st.session_state and page == "🔍 New Analysis":
    st.markdown("---")
    render_report(st.session_state["demo_result"])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: View single report from history
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "view_report":
    rid = st.session_state.get("view_report_id")
    report = get_report(rid) if rid else None
    if report:
        render_report(report)
    else:
        st.error("Report not found.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Report History
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Report History":
    st.markdown("## Analysis History")
    st.markdown("<p style='color:#64748b;margin-top:-12px;'>All saved due-diligence reports</p>", unsafe_allow_html=True)

    reports = list_reports(limit=50)
    if not reports:
        st.info("No analyses saved yet. Run a new analysis or load a demo.")
    else:
        for r in reports:
            risk = r["risk_level"]
            icon = {"high": "🔴", "medium": "🟡", "review": "🟢", "strong": "✅"}.get(risk, "⬜")
            badge = RISK_BADGE.get(risk, "")
            demo_note = " · <span style='color:#60a5fa;font-size:11px;'>DEMO</span>" if r["is_demo"] else ""
            col_info, col_btn = st.columns([5, 1])
            with col_info:
                st.markdown(f"""<div class="ts-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-weight:600;font-size:15px;">{r['project_name']}</span>
                            {f"<span style='color:#475569;margin-left:8px;font-family:IBM Plex Mono,monospace;font-size:12px;'>{r.get('token_ticker','')}</span>" if r.get('token_ticker') else ''}
                            {demo_note}
                        </div>
                        <div>{badge}</div>
                    </div>
                    <div style="color:#475569;font-size:12px;margin-top:8px;font-family:IBM Plex Mono,monospace;">
                        Score: {max(0,r['total_score'])}/85 · {r['created_at'][:10]} · ID: {r['report_id']}
                    </div>
                    <div style="color:#94a3b8;font-size:12px;margin-top:4px;">{r['recommendation']}</div>
                </div>""", unsafe_allow_html=True)
            with col_btn:
                if st.button("View →", key=f"view_{r['report_id']}", use_container_width=True):
                    st.session_state["view_report_id"] = r["report_id"]
                    st.session_state["page_override"] = "view_report"
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: How It Works
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📖 How It Works":
    st.markdown("## How TokenScope Risk Works")
    st.markdown("<p style='color:#64748b;margin-top:-12px;'>Architecture, methodology, and agent workflow</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class="ts-card">
    <b style="color:#3b82f6;">What this is</b><br>
    TokenScope Risk is an internal decision-support tool for crypto exchange listings, compliance, and trust & safety teams.
    It automates the initial due-diligence sweep of a token or project using public information, and produces a structured,
    explainable risk memo — not a chatbot response.
    </div>
    """, unsafe_allow_html=True)

    agents = [
        ("1", "Intake Agent", "Validates inputs. Identifies which sources were provided and which are missing. Sets the baseline for completeness scoring."),
        ("2", "Research Agent", "Scrapes the official website and documentation site. Extracts clean text using trafilatura. Handles errors gracefully."),
        ("3", "Document Agent", "Downloads and parses whitepaper PDFs using PyMuPDF. Falls back to HTML extraction if needed."),
        ("4", "GitHub Agent", "Queries the GitHub REST API for repo metadata: stars, forks, contributor count, last commit, language. Computes signal strength."),
        ("5", "Risk Review Agent", "Sends all source text to Claude with a structured prompt. Extracts: project summary, token utility, red flags, credibility signals. Evidence-backed only."),
        ("6", "Scoring Agent", "Computes 6 dimension scores + hype penalty via Claude. Sums to total. Maps to risk level. Fully explainable."),
        ("7", "Memo Writer Agent", "Generates the executive summary and analyst notes. Professional tone. Action-oriented. Never hallucinates."),
    ]

    for num, name, desc in agents:
        st.markdown(f"""<div class="ts-card" style="display:flex;gap:16px;align-items:flex-start;">
            <div style="background:#1e3a8a;color:#3b82f6;font-family:IBM Plex Mono,monospace;font-size:13px;font-weight:600;padding:6px 12px;border-radius:6px;min-width:32px;text-align:center;">{num}</div>
            <div>
                <div style="font-weight:600;color:#e2e8f0;">{name}</div>
                <div style="color:#94a3b8;font-size:13px;margin-top:4px;">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="ts-card" style="margin-top:20px;">
    <b style="color:#3b82f6;">Scoring Model</b><br><br>
    <table style="width:100%;font-size:13px;color:#94a3b8;">
    <tr><th style="text-align:left;color:#64748b;">Dimension</th><th style="color:#64748b;">Max</th></tr>
    <tr><td>Team Transparency</td><td>20</td></tr>
    <tr><td>Documentation Quality</td><td>15</td></tr>
    <tr><td>Token Utility Clarity</td><td>15</td></tr>
    <tr><td>GitHub / Engineering Signal</td><td>15</td></tr>
    <tr><td>Ecosystem Credibility</td><td>10</td></tr>
    <tr><td>Research Completeness</td><td>10</td></tr>
    <tr><td>Hype / Inconsistency Penalty</td><td>−15 max</td></tr>
    <tr style="color:#e2e8f0;"><td><b>Total</b></td><td><b>85</b></td></tr>
    </table><br>
    <b>0–29</b> = High Risk &nbsp;|&nbsp; <b>30–54</b> = Medium Risk &nbsp;|&nbsp; <b>55–74</b> = Review Further &nbsp;|&nbsp; <b>75+</b> = Strong Signal
    </div>
    """, unsafe_allow_html=True)
