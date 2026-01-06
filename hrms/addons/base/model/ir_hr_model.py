from sqlalchemy import Column, Integer, String, Text,ForeignKey
from sqlalchemy.orm import relationship
from hrms.core.utilities.database import Base


class IrHrModel(Base):
    __tablename__ = "ir_hr_model"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(128))
    module_name = Column(String(128), nullable=False)

    views = relationship("IrHrView", back_populates="model")