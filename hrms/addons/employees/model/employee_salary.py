from sqlalchemy import Column, Integer, ForeignKey,String, Enum
from hrms.addons.base.model.base_model import HRMSBase
import enum

class emp_bonus_enum(enum.Enum):
    PROVIDENDFUND = "Provident Fund"
    EIS= "Employee Investment Scheme"

class EmployeeSalary(HRMSBase):
    __tablename__ = "hr_salary"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"))
    basic_salary = Column(Integer, default=0)
    allowances = Column(Integer, default=0)
    deductions = Column(Integer, default=0)
    net_salary = Column(Integer, default=0)
    employee_bonus = Column(Enum(emp_bonus_enum, name="emp_bonus_enum"), nullable=True)