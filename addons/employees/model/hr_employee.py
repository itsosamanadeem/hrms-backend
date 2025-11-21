from sqlalchemy import Column, Integer, String, Text, ForeignKey
from core.utilities.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class HrEmployee(Base):
    __tablename__ = "hr_employee"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    emp_name = Column(String(128))
    email = Column(String(128), unique=True)
    phone = Column(String(15), unique=True)
    address = Column(Text)
    job_title = Column(String(128))
    dep_name = Column(String(128))

    attendance_ids = relationship("IrHrAttendance", back_populates="employee")

    # attendance_one2many = relationship(
    #     "IrHrAttendance",
    #     back_populates="employee_many2one",
    #     lazy="selectin"
    # )
