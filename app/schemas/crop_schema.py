from pydantic import BaseModel

class CropBase(BaseModel):
    name: str
    crop_type: str
    growth_stage: str
    health_score: float | None = 100.0
    farm_id: int

class CropCreate(CropBase):
    pass

class CropResponse(CropBase):
    id: int
    class Config:
        orm_mode = True
