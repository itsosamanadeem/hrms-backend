from sqlalchemy import Column, Integer, ForeignKey, String, Float
from hrms.addons.base.model.base_model import HRMSBase

class HrSalary(HRMSBase):
    __tablename__ = "hr_payroll"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    payroll = Column(Integer, default=0)
    amount = Column(Float, nullable=True, default=0.0)
    