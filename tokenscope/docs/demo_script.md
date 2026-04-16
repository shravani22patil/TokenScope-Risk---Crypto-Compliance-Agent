# TokenScope Risk — 2-Minute Demo Script

---

## Setup (before demo)
- App running at localhost:8501 (or Streamlit Cloud URL)
- Browser open on the New Analysis page
- No API key needed for demo mode

---

## Script (≈ 2 minutes)

**[0:00–0:15] — Hook**
> "This is TokenScope Risk — a 7-agent AI system that automates the initial due-diligence review
> for crypto token listings. Instead of an analyst spending 3 hours manually reading whitepapers
> and GitHub repos, TokenScope does it in under 2 minutes and produces a structured compliance memo."

**[0:15–0:30] — Load High-Risk Demo**
*Click: "🔴 High Risk Demo" button*
> "Let me show you the worst-case scenario first. This is MoonShard AI — a project with anonymous
> team, no GitHub, a 3-page whitepaper that says 'Tokenomics TBD', and '10,000x' marketing claims."

*Point to score gauge: shows near-zero*
> "Score: negative 12 out of 85. The system triggered maximum hype penalty and zero scores
> across every dimension. Recommendation: Do Not List."

**[0:30–0:50] — Walk through Risk Tab**
*Click: "⚠️ Risk Analysis" tab*
> "You can see 7 red flags, all tagged by severity and source reference. The scoring agent
> gives you a rationale for every dimension — this isn't vibes, it's evidence-backed scoring.
> Team Transparency: 0. GitHub Signal: 0. Utility Clarity: 0."

**[0:50–1:10] — Load Strong Signal Demo**
*Click: "← Back" then "✅ Strong Signal Demo"*
> "Now the opposite — Helios Protocol. Doxxed team, 1,200 GitHub stars, 34 contributors,
> two public audits, clear tokenomics. Score: 76 out of 85. The agent found credibility signals
> and flagged only one minor item."

*Point to radar chart*
> "The radar chart shows strong scores across all 6 positive dimensions."

**[1:10–1:30] — Evidence Explorer**
*Click: "📂 Evidence" tab*
> "Every piece of text the agent extracted is preserved here with the source. You can expand
> each source card to see exactly what the AI read — full traceability, no hallucination."

**[1:30–1:50] — Export Memo**
*Click: "📄 Export Memo" tab, then Download button*
> "One click exports a structured Markdown compliance memo — executive summary, dimension scores,
> red flags, missing information, analyst notes — ready to drop into your listings review workflow."

**[1:50–2:00] — Wrap**
> "The agent pipeline uses 7 separate Claude API calls — Intake, Research, Document, GitHub,
> Risk Review, Scoring, and Memo Writer — each with a focused prompt and typed output.
> The full code is on GitHub with a FastAPI backend, Pydantic schemas, SQLite report history,
> and a Streamlit Cloud deployment. Link in the description."

---

*Total: ~2 minutes. Adjust pacing to audience.*
