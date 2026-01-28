from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from hrms.addons.base.model.base_model import HRMSBase
from .group_role_rel import ir_hr_group_role_rel

class IrHrGroup(HRMSBase):
    __tablename__ = "ir_hr_group"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    category = Column(String(64))
    description = Column(Text)
    
    roles = relationship(
        "IrHrRole",
        secondary=ir_hr_group_role_rel,
        back_populates="groups"
    )