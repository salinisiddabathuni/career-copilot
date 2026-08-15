from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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