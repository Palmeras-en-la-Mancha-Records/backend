from pydantic import BaseModel, ConfigDict, Field

class DiscBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Título del disco o álbum")
    artist: str = Field(..., min_length=1, max_length=150, description="Artista o grupo musical")
    release_year: int | None = Field(default=None, ge=1900, le=2100, description="Año de publicación")
    genre: str | None = Field(default=None, max_length=100, description="Género musical")
    record_label: str | None = Field(default=None, max_length=100, description="Sello o discográfica")
    price: float = Field(default=0.0, ge=0.0, description="Precio del disco")
    cover_image_url: str | None = Field(default=None, description="URL o ruta de la portada")

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
