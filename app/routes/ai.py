from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.ai_service import route_crop_query
from ..config.settings import settings
import logging

router = APIRouter(prefix="/ai", tags=["AI"])
logger = logging.getLogger(__name__)

# 🔹 Request model for asking crop questions
class CropQuery(BaseModel):
    query: str
    crop_name: str
    kiswahili: bool = False  # Optional toggle for Kiswahili support

# 🔹 Request model for feedback
class Feedback(BaseModel):
    query: str
    crop_name: str
    rating: int  # 1 = bad, 2 = okay, 3 = good

# 🔹 In-memory feedback store (can be replaced with DB later)
feedback_store = []

# ✅ Structured analysis endpoint
@router.post("/analyze")
def analyze_crop_query(payload: CropQuery):
    if not settings.OPENROUTER_API_KEY:
        logger.error("Missing OpenRouter API key.")
        return {"response": "Missing OpenRouter API key."}
    try:
        result = route_crop_query(payload.query, payload.crop_name)
        return result
    except Exception as e:
        logger.exception("Error during crop analysis")
        return {"response": f"Backend error: {str(e)}"}

# ✅ General crop Q&A (ChatGPT-style)
@router.post("/ask")
def ask_crop_question(payload: CropQuery):
    if not settings.OPENROUTER_API_KEY:
        logger.error("Missing OpenRouter API key.")
        return {"response": "Missing OpenRouter API key."}
    try:
        result = route_crop_query(payload.query, payload.crop_name, kiswahili=payload.kiswahili)
        return result
    except Exception as e:
        logger.exception("Error during crop Q&A")
        return {"response": f"Backend error: {str(e)}"}

# ✅ Feedback endpoint
@router.post("/feedback")
def submit_feedback(payload: Feedback):
    feedback_store.append(payload.dict())
    logger.info(f"Feedback received: {payload.dict()}")
    return {"message": "Feedback received"}