from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from models.labels_models import Label
from schemas.labels import LabelCreate, LabelUpdate


# Read Operations
def get_all_labels(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Label]:

    try:
        return (
            db.query(Label)
            .offset(skip)
            .limit(limit)
            .all()
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving labels"
        )


def get_label_by_id(
    db: Session,
    label_id: int
) -> Label:

    try:
        label = (
            db.query(Label)
            .filter(Label.id == label_id)
            .first()
        )

        if label is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Label with id {label_id} not found"
            )

        return label

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving label"
        )


# Write Operations
def create_label(
    db: Session,
    label: LabelCreate
) -> Label:

    try:
        new_label = Label(
            name=label.name,
            country=label.country,
            website=label.website
        )

        db.add(new_label)
        db.commit()
        db.refresh(new_label)
        return new_label

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating label. The provided data violates a database constraint."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating label"
        )


def update_label(
    db: Session,
    label_id: int,
    label_update: LabelUpdate
) -> Label:

    try:
        db_label = get_label_by_id(
            db,
            label_id
        )

        update_data = label_update.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(db_label, field, value)
        db.commit()
        db.refresh(db_label)
        return db_label

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating label. The provided data violates a database constraint."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating label"
        )

def delete_label(
    db: Session,
    label_id: int
) -> None:

    try:
        db_label = get_label_by_id(
            db,
            label_id
        )

        db.delete(db_label)
        db.commit()

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting label. The label cannot be deleted because it is being used."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting label"
        )