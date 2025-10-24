from sqlalchemy.orm import Session
from ..models.farm import Farm
from ..schemas.farm_schema import FarmCreate, FarmUpdate 

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

def update_farm(db: Session, farm_id: int, data: FarmUpdate):
    farm = get_farm_by_id(db, farm_id)
    if not farm:
        return None

    for field, value in data.dict().items():
        setattr(farm, field, value)

    db.commit()
    db.refresh(farm)
    return farm

def delete_farm(db: Session, farm_id: int):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if farm:
        db.delete(farm)
        db.commit()