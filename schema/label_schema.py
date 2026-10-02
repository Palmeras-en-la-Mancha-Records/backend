from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class LabelBase(BaseModel):
    name: str = Field(..., example="Label Name")
    country: Optional[str] = Field(None, example="Country Name")
    website: Optional[str] = Field(None, example="https://www.labelwebsite.com")

class LabelRead(LabelBase):
    # from_attributes permite serializar objetos SQLAlchemy (ORM) directamente
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)