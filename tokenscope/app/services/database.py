"""
services/database.py
--------------------
SQLite persistence layer for TokenScope Risk.
Structured so PostgreSQL can be swapped in via DATABASE_URL env var.
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = os.getenv("DATABASE_URL", "app/data/tokenscope.db").replace("sqlite:///", "")


def _get_conn() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id     TEXT PRIMARY KEY,
                project_name  TEXT NOT NULL,
                token_ticker  TEXT,
                risk_level    TEXT NOT NULL,
                total_score   INTEGER NOT NULL,
                recommendation TEXT NOT NULL,
                created_at    TEXT NOT NULL,
                is_demo       INTEGER DEFAULT 0,
                demo_scenario TEXT,
                report_json   TEXT NOT NULL
            )
        """)
        conn.commit()
    print(f"✅ Database ready: {DB_PATH}")


def save_report(report_dict: dict) -> None:
    """Persist a full report dict to the database."""
    with _get_conn() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO reports
               (report_id, project_name, token_ticker, risk_level, total_score,
                recommendation, created_at, is_demo, demo_scenario, report_json)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                report_dict["report_id"],
                report_dict["project_name"],
                report_dict.get("token_ticker"),
                report_dict["scoring"]["risk_level"],
                report_dict["scoring"]["total_score"],
                report_dict["scoring"]["recommendation"],
                report_dict["created_at"],
                int(report_dict.get("is_demo", False)),
                report_dict.get("demo_scenario"),
                json.dumps(report_dict),
            ),
        )
        conn.commit()


def get_report(report_id: str) -> Optional[dict]:
    """Fetch a single report by ID."""
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT report_json FROM reports WHERE report_id = ?", (report_id,)
        ).fetchone()
    if row:
        return json.loads(row["report_json"])
    return None


def list_reports(limit: int = 50) -> list[dict]:
    """Return lightweight list of reports (no full JSON)."""
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT report_id, project_name, token_ticker, risk_level,
                      total_score, recommendation, created_at, is_demo, demo_scenario
               FROM reports ORDER BY created_at DESC LIMIT ?""",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def delete_report(report_id: str) -> bool:
    with _get_conn() as conn:
        cur = conn.execute("DELETE FROM reports WHERE report_id = ?", (report_id,))
        conn.commit()
        return cur.rowcount > 0
