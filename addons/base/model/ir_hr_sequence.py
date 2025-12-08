from sqlalchemy import Column, Integer, String, Boolean
from hrms.core.utilities.database import Base

class IrHrSequence(Base):
    __tablename__ = "ir_hr_sequence"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    prefix = Column(String(32))
    padding = Column(Integer, default=4)
    next_number = Column(Integer, default=1)
    active = Column(Boolean, default=True)
