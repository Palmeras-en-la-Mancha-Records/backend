from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from model.label_model import Label
from schema.label_schema import LabelBase, LabelCreate, LabelUpdate, LabelResponse

def get_all_labels(db: Session, skip: int = 0, limit: int = 100) -> List[LabelResponse]:
    try:
        return db.query(Label).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving labels: {str(error)}"
        )

def create_label(db: Session, label: LabelCreate) -> Label:

    new_label = Label(
        name=label.name,
        country=label.country,
        website=label.website
    )

    try:
        db.add(new_label)
        db.commit()
        db.refresh(new_label)
        return new_label
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error: {str(error)}"
        )
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating label: {str(error)}"
        )

def get_label_by_id(db: Session, label_id: int) -> LabelResponse:
    try:
        label = db.query(Label).filter(Label.id == label_id).first()
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Label with id {label_id} not found"
            )
        return label
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving label: {str(error)}"
        )

def update_label(db: Session, label_id: int, label_update: LabelUpdate) -> Label:

    db.director = get_label_by_id(db, label_id)

    update_data = label_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db.director, field, value)

    try:
        label = db.query(Label).filter(Label.id == label_id).first()
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Label with id {label_id} not found"
            )
        for key, value in update_data.items():
            setattr(label, key, value)
        db.commit()
        db.refresh(label)
        return label
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Integrity error: {str(error)}"
        )
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating label: {str(error)}"
        )

def delete_label(db: Session, label_id: int) -> dict:

    db.director = get_label_by_id(db, label_id)

    try:
        label = db.query(Label).filter(Label.id == label_id).first()
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Label with id {label_id} not found"
            )
        db.delete(label)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting label: {str(error)}"
        )