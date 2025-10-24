from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    crop_name: str
    growth_stage: str

class RecommendationResponse(BaseModel):
    health_score: float
    advice: str