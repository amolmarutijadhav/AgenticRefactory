from pydantic import BaseModel
from typing import List, Dict

class DetectionInput(BaseModel):
    codebase_path: str

class DetectionOutput(BaseModel):
    issues: List[str]
    llm_prompts: List[str]
    llm_responses: List[str]

# Similar models for RefactorInput, RefactorOutput, etc.
