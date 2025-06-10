from pydantic import BaseModel
from typing import List, Dict

class ContextData(BaseModel):
    description: str
    audience: str
    purpose: str

class InputSchema(BaseModel):
    generated_text: str
    evaluation_criteria: List[str]
    context_data: ContextData
    reference_data: str  # or file path / summary
    user_query: str
