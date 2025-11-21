from sqlalchemy import Column, Integer, ForeignKey, String
from core.utilities.database import Base

class HrSalary(Base):
    __tablename__ = "hr_payroll"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    payroll = Column(Integer, default=0)

    