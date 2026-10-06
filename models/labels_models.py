# Imports
from sqlalchemy import Column, Integer, String
from database.database import Base

# Models
class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), index=True, nullable=False, unique=True)
    country = Column(String(100), nullable=True)
    website = Column(String(300), nullable=True)

    def __repr__(self) -> str:
        return f"<Label(id={self.id}, name='{self.name}', country='{self.country}', website='{self.website}')>"