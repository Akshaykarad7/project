from pydantic import BaseModel
from typing import Dict, List

class ScoreDetail(BaseModel):
    score: int
    comment: str

class QualityReport(BaseModel):
    composite_score: int
    scores: Dict[str, ScoreDetail]
    suggestions: List[str]

class RelevanceReport(BaseModel):
    relevance_score: int
    scores: Dict[str, ScoreDetail]
    suggestions: List[str]

class OutputSchema(BaseModel):
    quality_report: QualityReport
    relevance_report: RelevanceReport

