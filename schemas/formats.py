# Imports
from pydantic import BaseModel, ConfigDict, Field

# Schemas
class FormatBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Physical format name"
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        description="Format description"
    )


class FormatCreate(FormatBase):
    pass


class FormatUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Physical format name"
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        description="Format description"
    )


class FormatResponse(FormatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)