# Imports
from pydantic import BaseModel, ConfigDict, Field

# Schemas
class BranchBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=30)

class BranchCreate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int

    model_config = ConfigDict(from_attributes=True)