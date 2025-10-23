from sqlalchemy.orm import Session
from ..models.farm import Farm
from ..schemas.farm_schema import FarmCreate

def create_farm(db: Session, data: FarmCreate):
    farm = Farm(**data.dict())
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

def get_farms(db: Session):
    return db.query(Farm).all()

def get_farm_by_id(db: Session, farm_id: int):
    return db.query(Farm).filter(Farm.id == farm_id).first()

def delete_farm(db: Session, farm_id: int):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if farm:
        db.delete(farm)
        db.commit()
