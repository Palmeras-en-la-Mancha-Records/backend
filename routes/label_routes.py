from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from model.label_model import Label
from schema.label_schema import LabelRead

router = APIRouter(
    prefix="/label",
    tags=["Label"]
)

@router.get("/", response_model=List[LabelRead])
def get_labels(db: Session = Depends(get_db)):
    labels = db.query(Label).all()
    return labels