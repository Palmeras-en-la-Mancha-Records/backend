from sqlalchemy import Column, Integer, String
from core.database import Base

class Branch(Base):
    __tablename__ = "formats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)