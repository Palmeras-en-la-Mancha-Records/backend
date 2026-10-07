# Imports
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.branches_models import Branch
from schemas.branches import BranchCreate, BranchUpdate

# Read Operations
def get_branches(
    db: Session
) -> list[Branch]:

    try:
        return (
            db.query(Branch)
            .order_by(Branch.id)
            .all()
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving branches"
        )


def get_branch(
    db: Session,
    branch_id: int
) -> Branch:

    try:
        branch_db = (
            db.query(Branch)
            .filter(Branch.id == branch_id)
            .first()
        )

        if branch_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )

        return branch_db

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving branch"
        )


# Write Operations
def create_branch(
    db: Session,
    branch_data: BranchCreate
) -> Branch:

    try:
        new_branch = Branch(
            **branch_data.model_dump()
        )

        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)

        return new_branch

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating branch"
        )


def update_branch(
    db: Session,
    branch_id: int,
    branch_data: BranchUpdate
) -> Branch:

    try:
        branch_db = (
            db.query(Branch)
            .filter(Branch.id == branch_id)
            .first()
        )

        if branch_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )

        update_dict = branch_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_dict.items():
            setattr(branch_db, key, value)

        db.commit()
        db.refresh(branch_db)

        return branch_db

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating branch"
        )


def delete_branch(
    db: Session,
    branch_id: int
) -> None:

    try:
        branch_db = (
            db.query(Branch)
            .filter(Branch.id == branch_id)
            .first()
        )

        if branch_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )

        db.delete(branch_db)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting branch"
        )
