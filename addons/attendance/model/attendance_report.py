from sqlalchemy import Column, String, ForeignKey, Integer, Double
from sqlalchemy.orm import relationship, mapped_column, Mapped
from core.utilities.database import Base

class IrHrAttendance(Base):
    __tablename__ = "ir_hr_attendance"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"))
    attendance= Column(Double)
    employee = relationship("HrEmployee", back_populates="attendance_ids")


