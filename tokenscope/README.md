# 🔍 TokenScope Risk
### Compliance & Listing Due-Diligence Agent
> An AI agent system for crypto project risk review, token listing research, and structured compliance intelligence.

---

## Problem Statement

Crypto exchanges, listing teams, and compliance analysts spend hours manually reviewing token projects — scraping websites, reading whitepapers, checking GitHub, and writing internal memos. This process is inconsistent, time-consuming, and often lacks structured evidence trails.

**TokenScope Risk** automates the initial due-diligence sweep using a 7-step AI agent pipeline, producing an explainable, evidence-backed risk score and downloadable compliance memo in minutes.

---

## Why This Matters in 2026

- Exchange listing teams face increasing regulatory pressure (MiCA, SEC scrutiny, FATF guidance)
- Trust & safety teams need systematic, documented review processes
- AI agent systems that produce structured, auditable outputs are exactly what compliance-conscious organizations need
- Generic chatbots don't cut it — this is a real decision-support tool

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                    │
│   Input Form → Agent Status → Risk Report → Export       │
└─────────────────────┬────────────────────────────────────┘
                       │
┌─────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend                         │
│   POST /analyze   GET /reports   POST /export/{id}       │
└─────────────────────┬────────────────────────────────────┘
                       │
┌─────────────────────▼────────────────────────────────────┐
│               Agent Orchestrator (orchestrator.py)       │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  Intake  │→ │ Research │→ │ Document │→ │GitHub  │  │
│  │  Agent   │  │  Agent   │  │  Agent   │  │Agent   │  │
│  └──────────┘  └──────────┘  └──────────┘  └────┬───┘  │
│                                                   │      │
│  ┌────────────┐  ┌─────────┐  ┌──────────────────▼──┐  │
│  │ Memo Writer│← │ Scoring │← │    Risk Review       │  │
│  │   Agent    │  │  Agent  │  │       Agent          │  │
│  └──────┬─────┘  └─────────┘  └─────────────────────┘  │
│         │                                                │
└─────────┼────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────┐
│              SQLite (→ PostgreSQL-ready)                  │
│              Report JSON + Metadata Storage              │
└──────────────────────────────────────────────────────────┘
```

---

## Agent Workflow

| # | Agent | Role |
|---|---|---|
| 1 | **Intake Agent** | Validates inputs, identifies missing sources |
| 2 | **Research Agent** | Scrapes website + docs using trafilatura |
| 3 | **Document Agent** | Parses whitepaper PDFs with PyMuPDF |
| 4 | **GitHub Agent** | Queries GitHub REST API for repo signals |
| 5 | **Risk Review Agent** | LLM-powered red flag detection (Claude) |
| 6 | **Scoring Agent** | Computes 7-dimension risk score (Claude) |
| 7 | **Memo Writer Agent** | Generates compliance memo text (Claude) |

**What makes this different from a chatbot:**
- Multi-step agent pipeline with explicit state passing
- Separate Claude calls per agent with focused prompts
- Tool use: real web scraping, PDF parsing, GitHub API
- Structured JSON outputs at every step
- Explainable, dimension-wise scoring (not vibes)
- Evidence-backed — never hallucinates

---

## Scoring Model

| Dimension | Max Score |
|---|---|
| Team Transparency | 20 |
| Documentation Quality | 15 |
| Token Utility Clarity | 15 |
| GitHub / Engineering Signal | 15 |
| Ecosystem Credibility | 10 |
| Research Completeness | 10 |
| Hype / Inconsistency Penalty | −15 max |
| **Total** | **85** |

Risk tiers: **0–29** = High Risk · **30–54** = Medium · **55–74** = Review · **75+** = Strong Signal

---

## Features

- ✅ 7-step multi-agent pipeline (no single mega-prompt)
- ✅ Live web scraping with graceful fallback
- ✅ PDF whitepaper parsing (PyMuPDF)
- ✅ GitHub API signals (stars, forks, contributors, last commit)
- ✅ Explainable dimension-wise scoring
- ✅ Red flag extraction with severity tagging
- ✅ Downloadable Markdown compliance memo
- ✅ SQLite report history (PostgreSQL-ready)
- ✅ 3 pre-built demo scenarios (strong / medium / high-risk)
- ✅ FastAPI backend + Streamlit frontend
- ✅ Premium dark-mode dashboard UI
- ✅ Structured JSON output at every stage

---

## Tech Stack

`Python 3.11` · `Anthropic Claude API` · `FastAPI` · `Streamlit` · `Pydantic` · `httpx` · `BeautifulSoup4` · `trafilatura` · `PyMuPDF` · `SQLite/SQLAlchemy` · `Plotly`

---

## Screenshots

> Run the app locally or on Streamlit Cloud to see the live dashboard.

| Overview | Risk Analysis |
|---|---|
| `screenshots/overview.png` | `screenshots/risk.png` |

| Evidence Explorer | Memo Export |
|---|---|
| `screenshots/evidence.png` | `screenshots/export.png` |

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourname/tokenscope-risk.git
cd tokenscope-risk

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 5. Run the Streamlit app
streamlit run streamlit_app.py
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ Yes | Claude API key |
| `GITHUB_TOKEN` | Optional | GitHub PAT (higher rate limits) |
| `DATABASE_URL` | Optional | SQLite path (default: `app/data/tokenscope.db`) |

---

## Running the FastAPI Backend

```bash
# Separately, for API-only usage
uvicorn app.main:app --reload --port 8000

# API docs at:
# http://localhost:8000/docs
```

---

## Deployment

### Option A: Streamlit Community Cloud (Fastest)
1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set main file: `streamlit_app.py`
4. Add `ANTHROPIC_API_KEY` in Secrets
5. Deploy — demo mode works without API key

### Option B: Vercel + Render (Production Signal)
- Frontend: Next.js rewrite on Vercel
- Backend: `uvicorn app.main:app` on Render (free tier)
- Set env vars in both platforms

---

## Folder Structure

```
tokenscope-risk/
├── streamlit_app.py          ← Main Streamlit UI
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── .streamlit/
│   └── config.toml           ← Dark theme
├── app/
│   ├── __init__.py
│   ├── main.py               ← FastAPI backend
│   ├── agents/
│   │   ├── __init__.py
│   │   └── orchestrator.py   ← 7-agent pipeline
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py       ← SQLite layer
│   │   ├── scraper.py        ← Web + PDF + GitHub
│   │   └── exporter.py       ← Markdown memo generator
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        ← All Pydantic schemas
│   ├── data/
│   │   ├── __init__.py
│   │   └── demo_data.py      ← 3 sample scenarios
│   └── utils/
│       └── __init__.py
├── tests/
├── docs/
└── notebooks/
```

---

## Resume Bullets

> ATS-optimized. Copy-paste ready.

1. **Built a 7-agent AI compliance pipeline** (Python, Anthropic Claude API, FastAPI) that automates token listing due-diligence for crypto exchanges; each agent performs a dedicated step—web scraping, PDF parsing, GitHub API analysis, LLM-powered red flag detection, and explainable dimension scoring—producing structured JSON reports with a downloadable compliance memo

2. **Designed and deployed a full-stack risk intelligence dashboard** (Streamlit, Plotly, SQLite) with a premium dark-mode UI featuring real-time agent status, radar/gauge score visualizations, source evidence explorer, and one-click report export; deployed on Streamlit Community Cloud with environment-variable-secured API key management

3. **Implemented an explainable 85-point risk scoring model** combining rule-based heuristics and LLM-assisted analysis across 7 dimensions (team transparency, documentation quality, GitHub signal, token utility clarity, ecosystem credibility, research completeness, and hype penalties), producing analyst-grade compliance memos for crypto listings and trust & safety teams

---

## Why This Project Is Relevant for AI Agent Roles

- **Agent orchestration**: 7 explicitly defined agents with typed state passing (not one big prompt)
- **Tool use**: Real web scraping, PDF parsing, GitHub REST API — not simulated
- **Structured outputs**: Pydantic schemas enforced at every layer
- **Explainability**: Every score has a rationale and evidence snippets
- **Production-ready**: FastAPI backend, SQLite storage, deployment config, error handling
- **Business utility**: Solves a real problem in crypto compliance — not a toy demo

---

## Future Roadmap

1. **LangGraph integration** — replace sequential agents with a proper DAG with retry/branch logic
2. **Vector retrieval** — ChromaDB for cross-report pattern matching ("similar to past high-risk projects")
3. **News API integration** — CryptoPanic or GDELT for recent sentiment signals
4. **Team verification layer** — LinkedIn + Twitter cross-referencing for doxxed team claims
5. **Audit trail signing** — cryptographic hash of each report for immutable audit log

---

*TokenScope Risk is a portfolio project. Demo data is simulated for demonstration purposes. Not financial or legal advice.*
