# Imports
from sqlalchemy import Column, Integer, String, Float
from core.database import Base

# Models
class Disc(Base):
    __tablename__ = "discs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    release_year = Column(Integer, nullable=True)
    genre = Column(String, index=True, nullable=True)
    record_label = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    stock = Column(Integer, nullable=True, default=0)
    format_id = Column(Integer, nullable=True)
    cover_image_url = Column(String, nullable=True)
