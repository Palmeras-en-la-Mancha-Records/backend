from fastapi import APIRouter, HTTPException, Depends, Path, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.labels import LabelCreate, LabelResponse, LabelUpdate
import controller.label_controller as label_controller

# Router Configuration
router = APIRouter(
    prefix="/labels",
    tags=["Labels"]
)

# Endpoints
@router.get(
    "/",
    response_model=list[LabelResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all labels",
    description="Get a list of all labels with optional pagination."
)
def get_all_labels(
    db: Session = Depends(get_db)
):
    return label_controller.get_all_labels(db)


@router.get(
    "/{label_id}",
    response_model=LabelResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a label by ID",
    description="Get a single label by its unique ID."
)
def get_label(
    label_id: int = Path(..., ge=1, description="The ID of the label to retrieve"),
    db: Session = Depends(get_db)
):
    label_db = label_controller.get_label_by_id(db, label_id)
    if label_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )  
    return label_db


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
    try:
        return label_controller.create_label(db, label_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put(
    "/{label_id}",
    response_model=LabelResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing label",
    description="Update the details of an existing label by its unique ID."
)
def update_existing_label(
    label_data: LabelUpdate,
    label_id: int = Path(..., ge=1, description="The ID of the label to update"),
    db: Session = Depends(get_db)
):
    try:
        label_db = label_controller.update_label(
            db=db,
            label_id=label_id,
            label_update=label_data
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    if label_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    return label_db


@router.delete(
    "/{label_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a label",
    description="Delete an existing label by its unique ID."
)
def delete_existing_label(
    label_id: int = Path(..., ge=1, description="The ID of the label to delete"),
    db: Session = Depends(get_db)
):
    deleted = label_controller.delete_label(db, label_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    return {"detail": "Label deleted successfully"}
