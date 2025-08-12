from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel


class Difficulty(str, Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"


class Meta(BaseModel):
    duration_ms: Optional[int] = None
    difficulty: Optional[Difficulty] = None


class SubmitAnswer(BaseModel):
    assessment_id: str
    question_id: str
    answer_text: str
    model_score: float
    rubric: Optional[Dict[str, Any]] = None
    meta: Optional[Meta] = None


class Answer(SubmitAnswer):
    id: int
