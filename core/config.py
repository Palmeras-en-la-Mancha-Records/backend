import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env (.env debe estar en la raíz de backend)
load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Palmeras en la Mancha API")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./palmeras.db")

settings = Settings()
