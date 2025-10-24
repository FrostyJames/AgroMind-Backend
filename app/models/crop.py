from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    crop_type = Column(String(100))
    growth_stage = Column(String(100))
    health_score = Column(Float, default=100.0)
    farm_id = Column(Integer, ForeignKey("farms.id"))

    farm = relationship("Farm", back_populates="crops")
