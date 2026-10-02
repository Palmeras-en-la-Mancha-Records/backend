
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models.models as models, schemas.schemas as schemas
from core.database import engine, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This creates the database file and the subsidiaries table
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Palmeras en la Mancha API")

# Permissions for the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=404, detail="Tienda no encontrada")

    for key, value in branch.model_dump().items():
        setattr(db_branch, key, value)
        
    db.commit()
    db.refresh(db_branch)
    return db_branch

@app.delete("/branches/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
        
    db.delete(db_branch)
    db.commit()
    return {"message": "Tienda eliminada correctamente"}