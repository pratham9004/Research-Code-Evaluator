from __future__ import annotations

from pydantic import BaseModel


class CompareRequest(BaseModel):
    problem_id: str
    language: str
    ai_name: str
    ai_code: str
    human_code: str
    experiment_type: str = "RESEARCH"
