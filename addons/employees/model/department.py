from sqlalchemy import Column, Integer, ForeignKey
from core.utilities.database import Base

class EmployeeDepartment(Base):
    __tablename__ = "employee_department"
    __table_args__ = {"extend_existing": True}

    department_id = Column(Integer, primary_key=True)