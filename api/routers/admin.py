from fastapi import APIRouter, Depends, HTTPException

from .. import db
from ..middleware.auth import require_api_key

router = APIRouter(prefix="/admin")


@router.patch("/answers/{assessment_id}/{answer_id}")
def override_answer(assessment_id: str, answer_id: int, body: dict, _=Depends(require_api_key)):
    entries = db.DB.get(assessment_id)
    if not entries:
        raise HTTPException(status_code=404, detail="assessment not found")
    for e in entries:
        if e.get("id") == answer_id:
            e.update(body)
            return e
    raise HTTPException(status_code=404, detail="answer not found")
