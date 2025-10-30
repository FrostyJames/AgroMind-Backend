from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..schemas.crop_schema import CropCreate, CropResponse
from ..services import crop_service
from ..services.ai_service import route_crop_query
import logging

router = APIRouter(prefix="/crops", tags=["Crops"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=CropResponse)
def create_crop(payload: CropCreate, db: Session = Depends(get_db)):
    """
    Create a crop record and analyze its health using the AI service.
    """
    crop = crop_service.create_crop(db, payload)

    try:
        # Use the AI service to analyze crop health
        prompt = f"Assess the health of {crop.name} at growth stage {crop.growth_stage}."
        ai_result = route_crop_query(prompt, crop.name)

        if isinstance(ai_result, dict):
            crop.health_score = ai_result.get("health_score", 75.0)
            advice = ai_result.get("advice", "No AI advice available.")
        else:
            crop.health_score = 75.0
            advice = "No AI advice available."

    except Exception as e:
        logger.exception("AI analysis failed")
        crop.health_score = 75.0
        advice = "AI service unavailable."

    db.commit()
    db.refresh(crop)

    response = CropResponse.from_orm(crop)
    response_dict = response.dict()
    response_dict["advice"] = advice
    return response_dict

@router.get("/", response_model=List[CropResponse])
def list_crops(db: Session = Depends(get_db)):
    """
    Retrieve all crops.
    """
    return crop_service.get_crops(db)

@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single crop by its ID.
    """
    crop = crop_service.get_crop_by_id(db, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop

@router.delete("/{crop_id}")
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """
    Delete a crop by its ID.
    """
    crop = crop_service.get_crop_by_id(db, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    crop_service.delete_crop(db, crop_id)
    return {"detail": f"Crop with ID {crop_id} deleted successfully."}