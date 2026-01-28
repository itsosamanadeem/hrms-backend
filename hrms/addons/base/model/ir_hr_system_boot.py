from sqlalchemy import Column, String,Boolean
from hrms.addons.base.model.base_model import HRMSBase

class IrHrSystemBootStrap(HRMSBase):
    __tablename__ = "ir_hr_system_bootstrap"

    key = Column(String, primary_key=True)
    completed = Column(Boolean, default=False, nullable=False)