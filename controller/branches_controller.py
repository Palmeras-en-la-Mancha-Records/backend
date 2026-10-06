# Imports
from sqlalchemy.orm import Session

from models.branches import Branch
from schemas.branches import BranchCreate, BranchUpdate

# Read Operations
def get_branches(db: Session) -> list[Branch]:
    return db.query(Branch).order_by(Branch.id).all()


def get_branch(db: Session, branch_id: int) -> Branch | None:
    return db.query(Branch).filter(Branch.id == branch_id).first()

# Write Operations
def create_branch(db: Session, branch_data: BranchCreate) -> Branch:
    new_branch = Branch(**branch_data.model_dump())
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return new_branch


def update_branch(db: Session, branch_id: int, branch_data: BranchUpdate) -> Branch | None:
    branch_db = get_branch(db, branch_id)
    if branch_db is None:
        return None

    update_dict = branch_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(branch_db, key, value)

    db.commit()
    db.refresh(branch_db)
    return branch_db


def delete_branch(db: Session, branch_id: int) -> bool:
    branch_db = get_branch(db, branch_id)
    if branch_db is None:
        return False

    db.delete(branch_db)
    db.commit()
    return True
