from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class OpportunityCreate(BaseModel):
    type: str
    title: str
    source: Optional[str] = "manual"
    skills_required: Optional[List[str]] = []
    deadline: Optional[date] = None
    url: Optional[str] = None

class OpportunityResponse(OpportunityCreate):
    id: int
    fetched_at: datetime

    class Config:
        from_attributes = True
class ResumeResponse(BaseModel):
    id: int
    filename: str
    extracted_skills: List[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True