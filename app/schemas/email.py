from pydantic import BaseModel
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

    class Config:
        from_attributes = True