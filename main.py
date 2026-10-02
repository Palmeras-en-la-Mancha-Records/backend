from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config_variable import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from routes.label_routes import label_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida (Lifespan).
    El esquema de la base de datos lo gestiona Alembic, no la aplicación.
    """
    yield
    # Lógica de cierre o limpieza (si fuera necesaria)


# Inicialización de la aplicación FastAPI
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan
)

# Configuración de CORS (permite que el frontend independiente haga peticiones)
app.add_middleware(
    CORSMiddleware,
    # Solo el origen, sin la ruta del archivo. En producción, lista explícita de dominios.
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Registrar el router de discográficas (label_routes) en la aplicación FastAPI
app.include_router(label_routes)

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Ruta raíz para comprobar que el servidor está online y redirigir a la documentación.
    """
    return {
        "status": "online",
        "message": f"Welcome to {APP_TITLE}",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }