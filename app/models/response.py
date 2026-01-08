from pydantic import BaseModel
from typing import List, Optional


class AnalysisResult(BaseModel):
    """AI analysis result structure for PDF template mapping"""

    summary: str
    tech_stack: List[str]
    key_contributions: List[str]
    code_quality: str
    project_tree: str


class CallbackPayload(BaseModel):
    """Payload sent to Spring's PATCH endpoint"""

    status: str  # "COMPLETED" or "FAILED"
    result: Optional[AnalysisResult] = None
    error_message: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """Immediate response for POST /analyze"""

    status: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ACCEPTED",
                "message": "Analysis queued for Report #100"
            }
        }
