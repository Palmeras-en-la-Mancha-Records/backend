# Imports
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


# Schemas
class FormatBase(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=2,
            max_length=100
        )
    ] = Field(
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
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=2,
            max_length=100
        )
    ] | None = None

    description: str | None = Field(
        default=None,
        max_length=255,
        description="Format description"
    )


class FormatResponse(FormatBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )