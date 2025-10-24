from pydantic import BaseModel
from typing import List, Optional
from .crop_schema import CropResponse

class FarmBase(BaseModel):
    name: str
    location: Optional[str] = None
    size_hectares: Optional[int] = None

class FarmCreate(FarmBase):
    pass

class FarmUpdate(FarmBase):
    """Used for updating farm records."""
    pass

class FarmResponse(FarmBase):
    id: int
    crops: List[CropResponse] = []

    class Config:
        orm_mode = True