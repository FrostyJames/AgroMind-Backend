from sqlalchemy.orm import Session
from ..models.crop import Crop
from ..schemas.crop_schema import CropCreate

def create_crop(db: Session, data: CropCreate):
    crop = Crop(**data.dict())
    db.add(crop)
    db.commit()
    db.refresh(crop)
    return crop

def get_crops(db: Session):
    return db.query(Crop).all()

def get_crop_by_id(db: Session, crop_id: int):
    return db.query(Crop).filter(Crop.id == crop_id).first()

def update_crop_health(db: Session, crop_id: int, health_score: float):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if crop:
        crop.health_score = health_score
        db.commit()
        db.refresh(crop)
    return crop

def delete_crop(db: Session, crop_id: int):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if crop:
        db.delete(crop)
        db.commit()
