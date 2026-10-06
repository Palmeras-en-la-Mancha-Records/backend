# Imports
from typing import List
from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.labels import LabelCreate, LabelResponse, LabelUpdate
import controller.label_controller as label_controller

# Router Configuration
router = APIRouter(
    prefix="/label",
    tags=["Label"]
)

# Endpoints
@router.get(
    "/",
    response_model=List[LabelResponse],
    summary="Retrieve all labels",
    description="Get a list of all labels in the database."
)
def get_all_labels(
    skip: int = Query(0, ge=0, description="The number of labels to skip"),
    limit: int = Query(100, ge=1, le=1000, description="The number of labels to retrieve"),
    db: Session = Depends(get_db)
):
    return label_controller.get_all_labels(db=db, skip=skip, limit=limit)


@router.get(
    "/{label_id}",
    response_model=LabelResponse,
    summary="Retrieve a label by ID",
    description="Get a single label by its unique ID."
)
def get_label(
    label_id: int = Path(..., ge=1, description="The ID of the label to retrieve"),
    db: Session = Depends(get_db)
):
    return label_controller.get_label_by_id(db=db, label_id=label_id)


@router.post(
    "/",
    response_model=LabelResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new label",
    description="Create a new label with the provided details."
)
def create_new_label(
    label_data: LabelCreate,
    db: Session = Depends(get_db)
):
    return label_controller.create_label(db=db, label=label_data)


@router.put(
    "/{label_id}",
    response_model=LabelResponse,
    summary="Update an existing label",
    description="Update the details of an existing label by its unique ID."
)
def update_existing_label(
    label_data: LabelUpdate,
    label_id: int = Path(..., ge=1, description="The ID of the label to update"),
    db: Session = Depends(get_db)
):
    return label_controller.update_label(db=db, label_id=label_id, label_update=label_data)


@router.delete(
    "/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a label",
    description="Delete an existing label by its unique ID."
)
def delete_existing_label(
    label_id: int = Path(..., ge=1, description="The ID of the label to delete"),
    db: Session = Depends(get_db)
):
    label_controller.delete_label(db=db, label_id=label_id)