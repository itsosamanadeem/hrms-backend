from sqlalchemy import Column, Integer, String, Text, ForeignKey
from hrms.core.utilities.database import Base

class IrHrReport(Base):
    __tablename__ = "ir_hr_report"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    report_type = Column(String(64))  # PDF, Excel, Dashboard, etc.
    template_path = Column(String(256))
    description = Column(Text)
