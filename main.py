# Imports
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine, SessionLocal
from core.config import settings
import models.branches_models as branch_models
import models.formats_models as format_models
import models.albums_models as album_models
from routers.albums import router as albums_router, discs_router
from routers.formats import router as formats_router
from routers.branches import router as branches_router

# Database Initial Seeding
def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(format_models.Format).count() == 0:
            default_formats = [
                format_models.Format(name="Vinilo LP", description="Edicion estandar en vinilo 12 pulgadas"),
                format_models.Format(name="CD Digipak", description="Edicion en disco compacto digipak"),
                format_models.Format(name="Cassette", description="Cinta de cassette vintage analogica"),
                format_models.Format(name="Vinilo 7 Single", description="Single de 7 pulgadas a 45 RPM"),
            ]
            db.add_all(default_formats)
            db.commit()
    except Exception as error:
        db.rollback()
        print(f"Error seeding initial formats: {error}")
    finally:
        db.close()

# Application Lifespan Configuration
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_initial_data()
    yield

# FastAPI Application & Middleware Configuration
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

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
