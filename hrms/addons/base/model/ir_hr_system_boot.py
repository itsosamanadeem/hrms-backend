from sqlalchemy import Column, String,Boolean
from hrms.core.utilities.database import Base

class IrHrSystemBootStrap(Base):
    __tablename__ = "ir_hr_system_bootstrap"

    key = Column(String, primary_key=True)
    completed = Column(Boolean, default=False, nullable=False)