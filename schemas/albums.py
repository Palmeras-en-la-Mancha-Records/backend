# Imports
from pydantic import BaseModel, ConfigDict, Field

# Schemas
class AlbumBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Title of the album")
    artist: str = Field(..., min_length=1, max_length=150, description="Artist or musical band")
    release_year: int | None = Field(default=None, ge=1900, le=2100, description="Release year")
    genre: str | None = Field(default=None, max_length=100, description="Musical genre")
    record_label: str | None = Field(default=None, max_length=100, description="Record label")
    price: float = Field(default=0.0, ge=0.0, description="Album price")
    stock: int | None = Field(default=0, ge=0, description="Available stock")
    format_id: int | None = Field(default=None, description="Format identifier")
    cover_image_url: str | None = Field(default=None, description="Cover image URL or path")

class AlbumCreate(AlbumBase):
    pass

class AlbumUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    artist: str | None = Field(default=None, min_length=1, max_length=150)
    release_year: int | None = Field(default=None, ge=1900, le=2100)
    genre: str | None = Field(default=None, max_length=100)
    record_label: str | None = Field(default=None, max_length=100)
    price: float | None = Field(default=None, ge=0.0)
    stock: int | None = Field(default=None, ge=0)
    format_id: int | None = None
    cover_image_url: str | None = None

class AlbumResponse(AlbumBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Aliases for backwards compatibility
DiscBase = AlbumBase
DiscCreate = AlbumCreate
DiscUpdate = AlbumUpdate
DiscResponse = AlbumResponse
