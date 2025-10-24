from pydantic import BaseModel
from typing import Optional

class CropBase(BaseModel):
    name: str
    crop_type: str
    growth_stage: str
    health_score: Optional[float] = 100.0
    farm_id: int

class CropCreate(CropBase):
    pass

class CropResponse(CropBase):
    id: int

    class Config:
        orm_mode = True