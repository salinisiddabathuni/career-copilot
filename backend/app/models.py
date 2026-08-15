from sqlalchemy import Column, Integer, String, Date, DateTime, ARRAY
from sqlalchemy.sql import func
from app.database import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)
    title = Column(String, nullable=False)
    source = Column(String(50), default="manual")
    skills_required = Column(ARRAY(String))
    deadline = Column(Date, nullable=True)
    url = Column(String, nullable=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    extracted_skills = Column(ARRAY(String))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())