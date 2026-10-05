from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class LabelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, example="Sony Music")
    country: Optional[str] = Field(None, min_length=1, max_length=100, example="España")
    website: Optional[str] = Field(None, min_length=1, max_length=300, example="https://www.sonymusic.es/")

class LabelCreate(LabelBase):
    pass

class LabelUpdate(LabelBase):
    name: Optional[str] = Field(None, min_length=1, max_length=150, example="Sony Music")
    country: Optional[str] = Field(None, min_length=1, max_length=100, example="España")
    website: Optional[str] = Field(None, min_length=1, max_length=300, example="https://www.sonymusic.es/")

class LabelResponse(LabelBase):
    id: int = Field(..., description="The unique identifier of the label", example=1)
    model_config = ConfigDict(from_attributes=True)