import enum
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Enum
from sqlalchemy.orm import relationship
from core.utilities.database import Base


class LeaveTypeEnum(enum.Enum):
    SICK = "Sick"
    ANNUAL = "Annual"
    HAJJ = "Hajj"


class IrHrAttendance(Base):
    __tablename__ = "hr_attendance"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    
    # Many2one → HrEmployee.id  
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)

    attendance = Column(Float, nullable=True)

    leaves_type = Column(Enum(LeaveTypeEnum), nullable=True)

    # Relationship to employee
    employee = relationship(
        "HrEmployee",
        back_populates="attendance_ids"
    )
