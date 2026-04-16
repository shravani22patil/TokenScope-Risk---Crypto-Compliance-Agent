# TokenScope Risk — Portfolio Presentation Checklists

---

## ✅ GitHub Presentation Checklist

### Repository Setup
- [ ] Repo name: `tokenscope-risk` (clean, professional)
- [ ] Description: "AI agent system for crypto compliance due-diligence | 7-step pipeline | Claude API | FastAPI + Streamlit"
- [ ] Topics: `ai-agents`, `crypto`, `compliance`, `fastapi`, `streamlit`, `anthropic`, `langchain`, `python`
- [ ] License: MIT
- [ ] README has hero image or screenshot at the top

### README Quality
- [ ] Problem statement in first 3 lines
- [ ] Architecture diagram (ASCII or image)
- [ ] Feature list with checkmarks
- [ ] Tech stack table
- [ ] One-command local setup instructions
- [ ] Environment variables table
- [ ] Screenshots placeholders (add real screenshots after first run)
- [ ] Deployment section for Streamlit Cloud

### Code Quality
- [ ] No hardcoded API keys anywhere
- [ ] `.env.example` committed (not `.env`)
- [ ] `.gitignore` excludes `.env`, `__pycache__`, `*.db`
- [ ] All imports resolve (no broken imports)
- [ ] No commented-out dead code
- [ ] Consistent naming throughout

### Demo Readiness
- [ ] Demo mode works without API key (3 pre-built scenarios)
- [ ] Screenshot: Overview dashboard
- [ ] Screenshot: Risk analysis tab with red flags
- [ ] Screenshot: Evidence explorer
- [ ] Screenshot: Score gauge and radar chart
- [ ] GIF or video optional but impressive

### Extra Signals
- [ ] GitHub Actions CI (optional: `flake8` or `pytest` on push)
- [ ] Dockerfile or docker-compose for backend (optional)
- [ ] `tests/` folder with at least 3 test functions
- [ ] Pinned version numbers in `requirements.txt`

---

## 📣 LinkedIn / Project Sharing Checklist

### Post Copy (Template)
```
Built something I'm proud of: TokenScope Risk 🔍

A 7-agent AI system that automates crypto compliance due-diligence for 
exchange listing teams.

Instead of analysts spending hours manually reading whitepapers and GitHub 
repos, TokenScope:
→ Scrapes websites + PDFs
→ Queries GitHub API for engineering signals
→ Runs LLM-powered red flag detection
→ Computes an explainable 85-point risk score
→ Exports a structured compliance memo

Built with: Python · Anthropic Claude API · FastAPI · Streamlit · Pydantic

🔗 Live demo: [Streamlit Cloud URL]
🔗 GitHub: [your repo URL]

Happy to discuss the agent architecture — it's 7 separate Claude calls with 
typed state passing, not one giant prompt.

#AI #Crypto #Compliance #Python #AIAgents #BuiltWithClaude
```

### LinkedIn Post Best Practices
- [ ] Post with at least one screenshot image (algorithm favors media)
- [ ] Tag relevant technologies (not people unless you know them)
- [ ] Mention the problem solved, not just the tech used
- [ ] Ask a genuine question at the end to prompt engagement
- [ ] Reply to every comment within 24 hours
- [ ] Cross-post to relevant Discord servers (AI builders, crypto dev communities)

### Application Cover Notes
```
I built TokenScope Risk, a multi-agent AI compliance tool for crypto listing 
teams. It uses a 7-step agent pipeline (Intake → Research → Document → GitHub 
→ Risk Review → Scoring → Memo Writer) to automate due-diligence and produce 
structured, explainable risk reports. The project demonstrates agent orchestration, 
real tool use (web scraping, PDF parsing, GitHub API), and production-ready 
architecture with FastAPI backend and Streamlit dashboard.
```

---

## 100-Word Project Description (for internship applications)

*Copy-paste into application forms, portfolio pages, or LinkedIn "Projects".*

> TokenScope Risk is an AI agent system that automates crypto token due-diligence for exchange 
> listing and compliance teams. A 7-step agent pipeline (built with Python and Anthropic's Claude API) 
> handles web scraping, PDF whitepaper parsing, GitHub API analysis, LLM-powered red flag detection, 
> and explainable 85-point risk scoring — producing a downloadable compliance memo per analysis. 
> The system uses FastAPI for the backend, Streamlit for the dashboard, SQLite for report storage, 
> and Pydantic for typed schemas. Three demo scenarios (strong, medium, high-risk) allow the app 
> to run without an API key. Deployed on Streamlit Community Cloud.
