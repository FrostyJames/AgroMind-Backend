from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    location = Column(String(120))
    size_hectares = Column(Integer)

    crops = relationship("Crop", back_populates="farm", cascade="all, delete")
