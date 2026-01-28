from sqlalchemy import Column, Integer, String, Text
from hrms.addons.base.model.base_model import HRMSBase
from sqlalchemy.orm import relationship
from .group_role_rel import ir_hr_group_role_rel

class IrHrRole(HRMSBase):
    __tablename__ = "ir_hr_role"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    code = Column(String(64), unique=True)
    description = Column(Text)
    permissions = Column(Text)  

    groups = relationship(
        "IrHrGroup",
        secondary=ir_hr_group_role_rel,
        back_populates="roles"
    )