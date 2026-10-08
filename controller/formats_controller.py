# Imports
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.formats_models import Format
from schemas.formats import FormatCreate, FormatUpdate


# Read Services
def get_formats(db: Session) -> list[Format]:
    try:
        return (
            db.query(Format)
            .order_by(Format.id)
            .all()
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving formats"
        )


def get_format(
    db: Session,
    format_id: int
) -> Format:

    try:
        format_db = (
            db.query(Format)
            .filter(Format.id == format_id)
            .first()
        )

        if format_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Format not found"
            )

        return format_db

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving format"
        )


def get_format_by_name(
    db: Session,
    name: str
) -> Format | None:

    try:
        return (
            db.query(Format)
            .filter(Format.name == name)
            .first()
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking format name"
        )


# Write Services
def create_format(
    db: Session,
    format_data: FormatCreate
) -> Format:

    try:
        existing_format = get_format_by_name(
            db,
            format_data.name
        )

        if existing_format:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A format with this name already exists"
            )

        new_format = Format(
            name=format_data.name,
            description=format_data.description
        )

        db.add(new_format)
        db.commit()
        db.refresh(new_format)

        return new_format

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating format"
        )


def update_format(
    db: Session,
    format_id: int,
    format_data: FormatUpdate
) -> Format:

    try:
        format_db = (
            db.query(Format)
            .filter(Format.id == format_id)
            .first()
        )

        if format_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Format not found"
            )

        if format_data.name is not None:
            existing_format = (
                db.query(Format)
                .filter(
                    Format.name == format_data.name,
                    Format.id != format_id
                )
                .first()
            )

            if existing_format:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A format with this name already exists"
                )

            format_db.name = format_data.name

        if format_data.description is not None:
            format_db.description = format_data.description

        db.commit()
        db.refresh(format_db)

        return format_db

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating format"
        )


def delete_format(
    db: Session,
    format_id: int
) -> None:

    try:
        format_db = (
            db.query(Format)
            .filter(Format.id == format_id)
            .first()
        )

        if format_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Format not found"
            )

        db.delete(format_db)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting format"
        )
