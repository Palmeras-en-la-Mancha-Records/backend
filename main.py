# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from core.config import settings
import models.models as models
import models.formats as format_models
import models.albums as album_models
from routers.albums import router as albums_router, discs_router
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
app.include_router(albums_router)
app.include_router(discs_router)
app.include_router(formats_router)
app.include_router(branches_router)
