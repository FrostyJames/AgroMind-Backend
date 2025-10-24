from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..schemas.farm_schema import FarmCreate, FarmUpdate, FarmResponse  # ✅ include FarmUpdate
from ..services import farm_service

router = APIRouter(prefix="/farms", tags=["Farms"])

@router.post("/", response_model=FarmResponse)
def create_farm(payload: FarmCreate, db: Session = Depends(get_db)):
    """Create a new farm record."""
    return farm_service.create_farm(db, payload)

@router.get("/", response_model=List[FarmResponse])
def list_farms(db: Session = Depends(get_db)):
    """Retrieve all farms."""
    return farm_service.get_farms(db)

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    """Retrieve a single farm by its ID."""
    farm = farm_service.get_farm_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: int, payload: FarmUpdate, db: Session = Depends(get_db)):
    """Update an existing farm record."""
    farm = farm_service.get_farm_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm_service.update_farm(db, farm_id, payload)

@router.delete("/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    """Delete a farm by its ID."""
    farm = farm_service.get_farm_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    farm_service.delete_farm(db, farm_id)
    return {"detail": f"Farm with ID {farm_id} deleted successfully."}