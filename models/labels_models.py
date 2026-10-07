from sqlalchemy import Column, Integer, String
from core.database import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), index=True, nullable=False, unique=True)
    country = Column(String(100), nullable=True)
    website = Column(String(300), nullable=True)