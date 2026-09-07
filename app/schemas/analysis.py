from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class EmailAnalysis(BaseModel):
    category: str
    priority: str
    sentiment: str
    intent: str
    summary: str
    key_information: List[str]

class EmailAnalysisResponse(EmailAnalysis):
    id: int
    email_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)