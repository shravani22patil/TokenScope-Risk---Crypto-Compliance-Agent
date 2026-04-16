"""
app/main.py
-----------
FastAPI backend for TokenScope Risk.
Exposes REST endpoints for analysis, report management, and export.

Run: uvicorn app.main:app --reload
"""

from __future__ import annotations
import json
import os
from datetime import datetime

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional

from .models.schemas import AnalysisRequest
from .services.database import init_db, save_report, get_report, list_reports, delete_report
from .services.exporter import generate_markdown_memo
from .data.demo_data import get_demo_report, all_demo_reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    for demo in all_demo_reports():
        save_report(demo)
    yield
    # Shutdown (nothing needed)


app = FastAPI(
    title="TokenScope Risk API",
    description="Compliance & Listing Due-Diligence Agent for crypto tokens",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "tokenscope-risk", "version": "1.0.0"}


@app.post("/analyze")
def analyze(request: AnalysisRequest):
    """
    Run the full 7-agent due-diligence pipeline.
    Returns the complete report dict.
    """
    if request.use_demo_data:
        scenario = request.demo_scenario or "medium"
        report = get_demo_report(scenario)
        save_report(report)
        return {"status": "complete", "report": report}

    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY not configured.")

    try:
        from .agents.orchestrator import run_analysis
        report = run_analysis(request)
        save_report(report)
        return {"status": "complete", "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports")
def get_reports(limit: int = 50):
    """List all saved reports (lightweight, no full JSON)."""
    return {"reports": list_reports(limit=limit)}


@app.get("/report/{report_id}")
def get_single_report(report_id: str):
    """Fetch a full report by ID."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.post("/export/{report_id}")
def export_report(report_id: str):
    """Generate and return a Markdown compliance memo."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    memo = generate_markdown_memo(report)
    return PlainTextResponse(content=memo, media_type="text/markdown")


@app.delete("/report/{report_id}")
def delete(report_id: str):
    """Delete a report by ID."""
    success = delete_report(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"deleted": report_id}
