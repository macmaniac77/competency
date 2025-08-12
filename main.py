import os
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

# When API_KEY is unset, auth checks are skipped.
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Control Assessment API", version="1.0.1")

BASE_DIR = Path(__file__).resolve().parent

# Simple in-memory store; replace with a DB for production
DB: Dict[str, List[Dict[str, Any]]] = {}

class Submit(BaseModel):
    assessment_id: str
    question_id: str
    answer_text: str
    model_score: float
    rubric: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

def require_auth(x_api_key: Optional[str] = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")


@app.get("/", include_in_schema=False)
def index():
    """Serve a tiny static page for manual testing."""
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/submit_answer")
def submit_answer(payload: Submit, x_api_key: Optional[str] = Header(None)):
    require_auth(x_api_key)
    DB.setdefault(payload.assessment_id, []).append(payload.model_dump())
    return {"accepted": True, "count": len(DB[payload.assessment_id])}

@app.get("/results")
def get_results(assessment_id: str, include_details: bool = False, x_api_key: Optional[str] = Header(None)):
    require_auth(x_api_key)
    entries = DB.get(assessment_id, [])
    total = len(entries)
    avg = (sum(e["model_score"] for e in entries) / total) if total else 0.0
    summary = {
        "basic_pct": _bucket(entries, "basic"),
        "intermediate_pct": _bucket(entries, "intermediate"),
        "advanced_pct": _bucket(entries, "advanced"),
    }
    out = {"assessment_id": assessment_id, "total": total, "avg_score": avg, "summary": summary}
    if include_details:
        out["details"] = entries
    return out

def _bucket(entries: List[Dict[str, Any]], level: str) -> float:
    xs = [e for e in entries if (e.get("meta") or {}).get("difficulty") == level]
    return round(100 * len(xs) / max(1, len(entries)), 1)
