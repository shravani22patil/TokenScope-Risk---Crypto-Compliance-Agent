"""
services/scraper.py
-------------------
Web content fetcher and text extractor.
Handles HTML pages, PDF whitepapers, and GitHub API metadata.
Fails gracefully — never crashes the agent pipeline.
"""

from __future__ import annotations
import os
import re
import time
from typing import Optional
import httpx

# Optional: trafilatura for clean text extraction
try:
    import trafilatura
    TRAFILATURA_OK = True
except ImportError:
    TRAFILATURA_OK = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_OK = True
except ImportError:
    PYMUPDF_OK = False

from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; TokenScopeBot/1.0; "
        "+https://github.com/tokenscope-risk)"
    )
}
TIMEOUT = 15
MAX_TEXT_CHARS = 12_000   # cap per source to keep context manageable


def fetch_url_text(url: str) -> tuple[str, Optional[str]]:
    """
    Fetch a web page and return (extracted_text, error_message).
    Uses trafilatura if available, falls back to BeautifulSoup.
    """
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
        html = resp.text

        if TRAFILATURA_OK:
            text = trafilatura.extract(
                html,
                include_tables=True,
                include_links=False,
                no_fallback=False,
            ) or ""
        else:
            soup = BeautifulSoup(html, "lxml")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)

        text = _clean(text)
        return text[:MAX_TEXT_CHARS], None

    except Exception as e:
        return "", str(e)


def fetch_pdf_text(url: str) -> tuple[str, Optional[str]]:
    """Download a PDF and extract text with PyMuPDF."""
    if not PYMUPDF_OK:
        return "", "PyMuPDF not available; PDF parsing skipped."
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=30, follow_redirects=True)
        resp.raise_for_status()
        doc = fitz.open(stream=resp.content, filetype="pdf")
        pages_text = []
        for i, page in enumerate(doc):
            if i > 30:  # cap at 30 pages
                break
            pages_text.append(page.get_text())
        text = _clean("\n".join(pages_text))
        return text[:MAX_TEXT_CHARS], None
    except Exception as e:
        return "", str(e)


def fetch_github_signals(github_url: str) -> dict:
    """
    Pull repo metadata from the GitHub REST API.
    Returns a dict matching GitHubSignals schema.
    """
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {**HEADERS}
    if token:
        headers["Authorization"] = f"token {token}"

    # Parse owner/repo from URL
    parts = github_url.rstrip("/").split("github.com/")
    if len(parts) < 2:
        return _github_fallback("Could not parse GitHub URL")
    owner_repo = parts[1].split("/")[:2]
    if len(owner_repo) < 2:
        return _github_fallback("Could not extract owner/repo from URL")

    api_url = f"https://api.github.com/repos/{owner_repo[0]}/{owner_repo[1]}"

    try:
        r = httpx.get(api_url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Contributor count (separate endpoint)
        contrib_count = 0
        try:
            cr = httpx.get(api_url + "/contributors?per_page=100&anon=1", headers=headers, timeout=8)
            if cr.status_code == 200:
                contrib_count = len(cr.json())
        except Exception:
            pass

        last_commit = data.get("pushed_at", "")[:10] if data.get("pushed_at") else None

        # Determine signal strength
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        active = _is_active(last_commit)
        strength = _signal_strength(stars, forks, contrib_count, active)

        notes = []
        if not active:
            notes.append("Last commit > 90 days ago — low engineering activity")
        if stars < 10:
            notes.append("Fewer than 10 stars — minimal community traction")
        if contrib_count < 3:
            notes.append("Fewer than 3 contributors — possible single-dev project")

        return {
            "repo_url": github_url,
            "stars": stars,
            "forks": forks,
            "open_issues": data.get("open_issues_count"),
            "last_commit_date": last_commit,
            "contributor_count": contrib_count,
            "language": data.get("language"),
            "is_active": active,
            "signal_strength": strength,
            "notes": notes,
        }
    except Exception as e:
        return _github_fallback(str(e))


def _is_active(last_commit: Optional[str]) -> bool:
    if not last_commit:
        return False
    from datetime import date, timedelta
    try:
        d = date.fromisoformat(last_commit)
        return (date.today() - d).days <= 90
    except Exception:
        return False


def _signal_strength(stars: int, forks: int, contribs: int, active: bool) -> str:
    score = 0
    if stars > 500: score += 3
    elif stars > 100: score += 2
    elif stars > 20: score += 1
    if forks > 50: score += 2
    elif forks > 10: score += 1
    if contribs > 10: score += 2
    elif contribs > 3: score += 1
    if active: score += 2
    if score >= 6: return "strong"
    if score >= 3: return "moderate"
    return "weak"


def _github_fallback(error: str) -> dict:
    return {
        "repo_url": None,
        "stars": None,
        "forks": None,
        "open_issues": None,
        "last_commit_date": None,
        "contributor_count": None,
        "language": None,
        "is_active": False,
        "signal_strength": "unknown",
        "notes": [f"GitHub data unavailable: {error}"],
    }


def _clean(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r"\s{3,}", "  ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
