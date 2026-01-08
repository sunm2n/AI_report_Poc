from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    """Request schema for POST /analyze"""

    repo_url: str
    branch: str = "main"
    target_user: str
    report_id: int
    callback_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/myongji-univ/shuttle-bus.git",
                "branch": "main",
                "target_user": "HandsomeGuy",
                "report_id": 100,
                "callback_url": "http://spring-server/api/reports/100"
            }
        }
