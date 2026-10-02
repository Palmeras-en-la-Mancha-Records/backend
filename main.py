from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

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

@app.get("/")
def read_root():
    return {"message": "API de Palmeras en la Mancha Records funcionando"}