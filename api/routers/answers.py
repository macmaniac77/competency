from fastapi import APIRouter, Depends

from .. import db
from ..models import SubmitAnswer
from ..middleware.auth import require_api_key

router = APIRouter()


@router.post("/submit_answer")
def submit_answer(payload: SubmitAnswer, _=Depends(require_api_key)):
    db.ANSWER_SEQ += 1
    entry = payload.model_dump()
    entry["id"] = db.ANSWER_SEQ
    db.DB.setdefault(payload.assessment_id, []).append(entry)
    return {"accepted": True, "count": len(db.DB[payload.assessment_id])}
