# Imports
from pydantic import BaseModel, ConfigDict

# Schemas
class BranchBase(BaseModel):
    name: str
    address: str
    phone: str

class BranchCreate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int

    model_config = ConfigDict(from_attributes=True)