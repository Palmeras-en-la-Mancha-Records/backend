from sqlalchemy import Column, Integer, String
from core.database import Base

class Format(Base):
    __tablename__ = "formats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(String(255), nullable=True)