from typing import Dict, Any, List
from fastapi import APIRouter, Depends

from .. import db
from ..middleware.auth import require_api_key

router = APIRouter()


def _bucket(entries: List[Dict[str, Any]], level: str) -> float:
    xs = [e for e in entries if (e.get("meta") or {}).get("difficulty") == level]
    return round(100 * len(xs) / max(1, len(entries)), 1)


@router.get("/results")
def get_results(assessment_id: str, include_details: bool = False, _=Depends(require_api_key)):
    entries = db.DB.get(assessment_id, [])
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


@router.get("/sessions")
def list_sessions(_=Depends(require_api_key)):
    payload = []
    for aid, entries in db.DB.items():
        total = len(entries)
        avg = (sum(e["model_score"] for e in entries) / total) if total else 0.0
        payload.append({"assessment_id": aid, "total": total, "avg_score": avg})
    return payload


@router.get("/sessions/{assessment_id}")
def get_session(assessment_id: str, _=Depends(require_api_key)):
    return {"assessment_id": assessment_id, "answers": db.DB.get(assessment_id, [])}


@router.get("/export/csv")
def export_csv(assessment_id: str, _=Depends(require_api_key)):
    entries = db.DB.get(assessment_id, [])
    if not entries:
        return ""
    import csv
    from io import StringIO

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=entries[0].keys())
    writer.writeheader()
    writer.writerows(entries)
    return buf.getvalue()
