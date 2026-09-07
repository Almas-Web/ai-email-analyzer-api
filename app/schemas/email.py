from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EmailCreate(BaseModel):
    sender: str
    subject: str
    body: str

class EmailResponse(BaseModel):
    id: int
    user_id: int
    sender: str
    subject: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)