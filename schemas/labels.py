from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

#Schemas
class LabelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, description="Name of the record label")
    country: Optional[str] = Field(None, min_length=1, max_length=100, description="Country of origin")
    website: Optional[str] = Field(None, min_length=1, max_length=300, description="Official website URL")

class LabelCreate(LabelBase):
    pass

class LabelUpdate(LabelBase):
    name: str | None = Field(default=None, min_length=1, max_length=150, description="Name of the record label")
    country: str | None = Field(default=None, min_length=1, max_length=100, description="Country of origin")
    website: str | None = Field(default=None, min_length=1, max_length=300, description="Official website URL")

class LabelResponse(LabelBase):
    id: int = Field(..., description="The unique identifier of the label", json_schema_extra={"example": 1})
    model_config = ConfigDict(from_attributes=True)