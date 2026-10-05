# Imports
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from core.database import Base, engine, get_db
from core.config import settings
import models.models as models
import models.formats as format_models
import models.discs as disc_models
import schemas.schemas as schemas
from routers.discs import router as discs_router
from routers.formats import router as formats_router

# Database Initialization
Base.metadata.create_all(bind=engine)

# FastAPI Application & Middleware Configuration
app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Registration
app.include_router(discs_router)
app.include_router(formats_router)

# Branch Endpoints
@app.get("/branches/", response_model=list[schemas.BranchResponse])
def read_branches(db: Session = Depends(get_db)):
    branches = db.query(models.Branch).all()
    return branches

@app.post("/branches/", response_model=schemas.BranchResponse)
def create_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    db_branch = models.Branch(**branch.model_dump())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

@app.put("/branches/{branch_id}", response_model=schemas.BranchResponse)
def update_branch(branch_id: int, branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Store not found")

    for key, value in branch.model_dump().items():
        setattr(db_branch, key, value)
        
    db.commit()
    db.refresh(db_branch)
    return db_branch

@app.delete("/branches/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Store not found")
        
    db.delete(db_branch)
    db.commit()
    return {"message": "Store successfully deleted"}