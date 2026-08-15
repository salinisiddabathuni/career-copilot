from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from pypdf import PdfReader
import docx
import io
from app.ai_client import extract_skills

app = FastAPI()
from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.post("/opportunities", response_model=schemas.OpportunityResponse)
def create_opportunity(opportunity: schemas.OpportunityCreate, db: Session = Depends(get_db)):
    new_opportunity = models.Opportunity(**opportunity.model_dump())
    db.add(new_opportunity)
    db.commit()
    db.refresh(new_opportunity)
    return new_opportunity


@app.get("/opportunities", response_model=list[schemas.OpportunityResponse])
def get_opportunities(db: Session = Depends(get_db)):
    return db.query(models.Opportunity).all()
@app.post("/resume/upload", response_model=schemas.ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(contents))
        full_text = [p.text for p in doc.paragraphs if p.text.strip()]
        extracted_text = "\n".join(full_text)

    elif filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(contents))
        full_text = [page.extract_text() for page in reader.pages if page.extract_text()]
        extracted_text = "\n".join(full_text)

    else:
        return {"error": "Unsupported file type. Please upload a .docx or .pdf file."}

    skills = extract_skills(extracted_text)

    new_resume = models.Resume(filename=file.filename, extracted_skills=skills)
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume
@app.get("/resumes", response_model=list[schemas.ResumeResponse])
def get_resumes(db: Session = Depends(get_db)):
    return db.query(models.Resume).all()