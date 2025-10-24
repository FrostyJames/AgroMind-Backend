from fastapi import APIRouter
from ..schemas.recommendation_schema import RecommendationRequest, RecommendationResponse
from ..services.ai_service import analyze_crop_health

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("/", response_model=RecommendationResponse)
def get_recommendation(payload: RecommendationRequest):
    return analyze_crop_health(payload.crop_name, payload.growth_stage)