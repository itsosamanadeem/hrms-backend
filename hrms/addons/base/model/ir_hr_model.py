from sqlalchemy import Column, Integer, String, Text,ForeignKey
from sqlalchemy.orm import relationship
from hrms.addons.base.model.base_model import HRMSBase


class IrHrModel(HRMSBase):
    __tablename__ = "ir_hr_model"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(128))
    module_name = Column(String(128), nullable=False)

    views = relationship("IrHrView", back_populates="model")