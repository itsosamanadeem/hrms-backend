import enum
from sqlalchemy import Column, Integer, String, Text, Enum
from hrms.core.utilities.database import Base
from sqlalchemy.orm import relationship


class EmpTypeEnum(enum.Enum):
    CONTRACT = "CONTRACT"
    PERMANENT = "PERMANENT"


class EmpGroupLevel(enum.Enum):
    G1 = "GROUP-1"
    G2 = "GROUP-2"


class HrEmployee(Base):
    __tablename__ = "hr_employee"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    emp_name = Column(String(128))
    email = Column(String(128), unique=True)
    phone = Column(String(15), unique=True)

    # column names cannot have spaces
    second_phone = Column("Another Phonenumber", String(15), unique=True)

    # CORRECT ENUM
    status = Column(
        Enum(
            "draft",
            "submitted",
            "approved",
            "rejected",
            name="status_enum",  # PostgreSQL ENUM name
        ),
        nullable=True,
    )

    address = Column(Text)
    job_title = Column(String(128))
    dep_name = Column(String(128))

    # CORRECT named enums
    employee_type = Column(
        Enum(EmpTypeEnum, name="employee_type_enum"),
        nullable=True,
    )

    employee_group_type = Column(
        Enum(EmpGroupLevel, name="employee_group_type_enum"),
        nullable=True,
    )

    attendance_ids = relationship(
        "IrHrAttendance",
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    expense = relationship('Expense', back_populates='employee',cascade="all, delete-orphan")
    
    def __rep__(self):
        return f"Employee {self.id}"