import enum
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Enum, Boolean
from sqlalchemy.orm import relationship
from hrms.core.utilities.database import Base


class LeaveTypeEnum(enum.Enum):
    SICK = "Sick"
    ANNUAL = "Annual"
    HAJJ = "Hajj"


class IrHrAttendance(Base):
    __tablename__ = "hr_attendance"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)

    attendance = Column(Float, nullable=True)

    leaves_type = Column(Enum(LeaveTypeEnum), nullable=True)

    attendance_left = Column(Float, nullable=True)
    
    attendance_taken = Column(Boolean, default=False)
    
    employee = relationship(
        "HrEmployee",
        back_populates="attendance_ids"
    )
