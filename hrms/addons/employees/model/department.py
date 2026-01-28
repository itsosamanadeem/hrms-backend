from sqlalchemy import Column, Integer, ForeignKey
from hrms.addons.base.model.base_model import HRMSBase

class EmployeeDepartment(HRMSBase):
    __tablename__ = "employee_department"
    __table_args__ = {"extend_existing": True}

    department_id = Column(Integer, primary_key=True)