# Imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.branches import BranchCreate, BranchResponse, BranchUpdate
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
    branch = get_branch(db, branch_id)
    if branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )
    return branch


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
    branch = update_branch(db, branch_id, branch_data)
    if branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )
    return branch


@router.delete(
    "/{branch_id}",
    status_code=status.HTTP_200_OK
)
def delete_existing_branch(
    branch_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_branch(db, branch_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found"
        )
    return {
        "message": "Branch successfully deleted"
    }