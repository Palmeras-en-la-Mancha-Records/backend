from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.formats import (
    FormatCreate,
    FormatResponse,
    FormatUpdate
)
from services.formats_services import (
    create_format,
    delete_format,
    get_format,
    get_formats,
    update_format
)


router = APIRouter(
    prefix="/formats",
    tags=["Formats"]
)


@router.get(
    "/",
    response_model=list[FormatResponse],
    status_code=status.HTTP_200_OK
)
def read_formats(
    db: Session = Depends(get_db)
):
    return get_formats(db)


@router.get(
    "/{format_id}",
    response_model=FormatResponse,
    status_code=status.HTTP_200_OK
)
def read_format(
    format_id: int,
    db: Session = Depends(get_db)
):
    format_db = get_format(db, format_id)

    if format_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Format not found"
        )

    return format_db


@router.post(
    "/",
    response_model=FormatResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_format(
    format_data: FormatCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_format(db, format_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put(
    "/{format_id}",
    response_model=FormatResponse,
    status_code=status.HTTP_200_OK
)
def update_existing_format(
    format_id: int,
    format_data: FormatUpdate,
    db: Session = Depends(get_db)
):
    try:
        format_db = update_format(
            db,
            format_id,
            format_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    if format_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Format not found"
        )

    return format_db


@router.delete(
    "/{format_id}",
    status_code=status.HTTP_200_OK
)
def delete_existing_format(
    format_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_format(db, format_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Format not found"
        )

    return {
        "message": "Format deleted successfully"
    }