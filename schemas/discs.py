# Imports
from pydantic import BaseModel, ConfigDict, Field

# Schemas
class DiscBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Title of the disc or album")
    artist: str = Field(..., min_length=1, max_length=150, description="Artist or musical band")
    release_year: int | None = Field(default=None, ge=1900, le=2100, description="Release year")
    genre: str | None = Field(default=None, max_length=100, description="Musical genre")
    record_label: str | None = Field(default=None, max_length=100, description="Record label")
    price: float = Field(default=0.0, ge=0.0, description="Disc price")
    cover_image_url: str | None = Field(default=None, description="Cover image URL or path")

class DiscCreate(DiscBase):
    pass

class DiscUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    artist: str | None = Field(default=None, min_length=1, max_length=150)
    release_year: int | None = Field(default=None, ge=1900, le=2100)
    genre: str | None = Field(default=None, max_length=100)
    record_label: str | None = Field(default=None, max_length=100)
    price: float | None = Field(default=None, ge=0.0)
    cover_image_url: str | None = None

class DiscResponse(DiscBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
