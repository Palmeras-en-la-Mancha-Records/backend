# Imports
import os
from dotenv import load_dotenv

# Environment Configuration
load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Palmeras en la Mancha API")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./palmeras.db")

settings = Settings()
