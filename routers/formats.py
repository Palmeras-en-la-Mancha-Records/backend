# Imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.formats import (
    FormatCreate,
    FormatResponse,
    FormatUpdate
)
from controller.formats_controller import (
    create_format,
    delete_format,
    get_format,
    get_formats,
    update_format
)

# Router Configuration
router = APIRouter(
    prefix="/formats",
    tags=["Formats"]
)

# Endpoints
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
    return get_format(db, format_id)


@router.post(
    "/",
    response_model=FormatResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_format(
    format_data: FormatCreate,
    db: Session = Depends(get_db)
):
    return create_format(db, format_data)


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
    return update_format(
        db,
        format_id,
        format_data
    )


@router.delete(
    "/{format_id}",
    status_code=status.HTTP_200_OK
)
def delete_existing_format(
    format_id: int,
    db: Session = Depends(get_db)
):
    delete_format(db, format_id)

    return {
        "message": "Format deleted successfully"
    }
