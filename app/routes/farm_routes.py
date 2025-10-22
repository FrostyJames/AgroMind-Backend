from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas.farm_schema import FarmCreate, FarmResponse
from ..services import farm_service

router = APIRouter(prefix="/farms", tags=["Farms"])

@router.post("/", response_model=FarmResponse)
def create_farm(payload: FarmCreate, db: Session = Depends(get_db)):
    return farm_service.create_farm(db, payload)

@router.get("/", response_model=list[FarmResponse])
def list_farms(db: Session = Depends(get_db)):
    return farm_service.get_farms(db)

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = farm_service.get_farm_by_id(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@router.delete("/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    farm_service.delete_farm(db, farm_id)
    return {"detail": "Farm deleted"}
