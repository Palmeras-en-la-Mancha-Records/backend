# Imports
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from core.database import Base, engine, get_db
from core.config import settings
import models.models as models
import models.formats as format_models
import models.discs as disc_models
from routers.discs import router as discs_router
from routers.formats import router as formats_router
from routers.branches import router as branches_router


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
app.include_router(branches_router)

