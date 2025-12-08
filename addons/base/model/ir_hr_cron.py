from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from hrms.core.utilities.database import Base

class IrHrCron(Base):
    __tablename__ = "ir_hr_cron"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    model = Column(String(128))
    method = Column(String(128))
    interval_type = Column(String(32))  # minutes, hours, days
    interval_number = Column(Integer, default=1)
    nextcall = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
