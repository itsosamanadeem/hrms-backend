from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from hrms.addons.base.model.base_model import HRMSBase

class IrHrLog(HRMSBase):
    __tablename__ = "ir_hr_log"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    level = Column(String(16))  # INFO, WARN, ERROR
    message = Column(Text)
    create_date = Column(DateTime, default=datetime.utcnow)
