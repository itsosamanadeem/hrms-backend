from sqlalchemy import Column, Integer,ForeignKey, String
from sqlalchemy.orm import relationship
from hrms.addons.base.model.base_model import HRMSBase

class Expense(HRMSBase):

    __tablename__ = "hr_expense"
    __table_args__ = {"extend_existing": True}

    expense_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('hr_employee.id'))
    amount = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    employee = relationship('HrEmployee', back_populates='expense')
