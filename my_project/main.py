from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=List[schemas.TopProductSchema])
def read_top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity")
def read_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    data = crud.get_channel_activity(db, channel_name)
    return [{"date": row[0], "count": row[1]} for row in data]

@app.get("/api/search/messages", response_model=List[schemas.MessageSchema])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)
