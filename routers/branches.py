# Imports
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.branches import (
    BranchCreate,
    BranchResponse,
    BranchUpdate
)
from controller.branches_controller import (
    create_branch,
    delete_branch,
    get_branch,
    get_branches,
    update_branch,
)

# Router Configuration
router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)

# Endpoints
@router.get(
    "/",
    response_model=list[BranchResponse],
    status_code=status.HTTP_200_OK
)
def read_branches(
    db: Session = Depends(get_db)
):
    return get_branches(db)


@router.get(
    "/{branch_id}",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK
)
def read_branch(
    branch_id: int,
    db: Session = Depends(get_db)
):
    return get_branch(db, branch_id)


@router.post(
    "/",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_branch(
    branch_data: BranchCreate,
    db: Session = Depends(get_db)
):
    return create_branch(db, branch_data)


@router.put(
    "/{branch_id}",
    response_model=BranchResponse,
    status_code=status.HTTP_200_OK
)
def update_existing_branch(
    branch_id: int,
    branch_data: BranchUpdate,
    db: Session = Depends(get_db)
):
    return update_branch(
        db,
        branch_id,
        branch_data
    )


@router.delete(
    "/{branch_id}",
    status_code=status.HTTP_200_OK
)
def delete_existing_branch(
    branch_id: int,
    db: Session = Depends(get_db)
):
    delete_branch(db, branch_id)

    return {
        "message": "Branch successfully deleted"
    }