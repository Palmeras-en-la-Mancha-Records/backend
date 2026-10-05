from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
import models.models as models
import schemas.branches as schemas

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/", response_model=list[schemas.BranchResponse])
def read_branches(db: Session = Depends(get_db)):
    branches = db.query(models.Branch).all()
    return branches


@router.post("/", response_model=schemas.BranchResponse, status_code=201)
def create_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    db_branch = models.Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


@router.put("/{branch_id}", response_model=schemas.BranchResponse)
def update_branch(branch_id: int, branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()

    if db_branch is None:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")

    for key, value in branch.model_dump().items():
        setattr(db_branch, key, value)

    db.commit()
    db.refresh(db_branch)
    return db_branch


@router.delete("/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()

    if db_branch is None:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")

    db.delete(db_branch)
    db.commit()
    return {"message": "Tienda eliminada correctamente"}