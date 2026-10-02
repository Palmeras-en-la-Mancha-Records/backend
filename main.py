from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esto crea el archivo de la base de datos y la tabla de filiales
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Palmeras en la Mancha API")

# Permisos para que el frontend pueda hablar con este backend
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