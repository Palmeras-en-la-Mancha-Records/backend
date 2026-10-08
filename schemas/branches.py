# Imports
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


# Schemas
class BranchBase(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=100
        )
    ]

    address: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=255
        )
    ]

    phone: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=30
        )
    ]


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=100
        )
    ] | None = None

    address: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=255
        )
    ] | None = None

    phone: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=30
        )
    ] | None = None


class BranchResponse(BranchBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )