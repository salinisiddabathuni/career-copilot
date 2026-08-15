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