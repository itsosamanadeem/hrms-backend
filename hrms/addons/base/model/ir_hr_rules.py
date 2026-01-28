from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from hrms.addons.base.model.base_model import HRMSBase

class IrHrRule(HRMSBase):
    __tablename__ = "ir_hr_rule"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    domain_filter = Column(Text)   # JSON or domain expression
    global_rule = Column(Boolean, default=False)
