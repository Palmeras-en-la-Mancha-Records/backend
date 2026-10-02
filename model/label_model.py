from sqlalchemy import Column, Integer, String
from database.database import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    website = Column(String)

    def __repr__(self) -> str:
        return f"<Label(id={self.id}, name='{self.name}', country='{self.country}', website='{self.website}')>"