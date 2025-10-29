from fastapi import APIRouter
from ..schemas.recommendation_schema import RecommendationRequest, RecommendationResponse
from ..services.ai_service import route_crop_query

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("/", response_model=RecommendationResponse)
def get_recommendation(payload: RecommendationRequest):
    query = f"analyze health of {payload.crop_name} at {payload.growth_stage}"
    result = route_crop_query(query, payload.crop_name)

    # Normalize response to match RecommendationResponse schema
    return RecommendationResponse(
        health_score=result.get("health_score", 75.0),
        advice=result.get("advice", "No advice returned.")
    )