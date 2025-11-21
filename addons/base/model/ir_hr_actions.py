from sqlalchemy import Column, Integer, String, ForeignKey, Text
from core.utilities.database import Base

class IrHrAction(Base):
    __tablename__ = "ir_hr_action"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(String(64))  # 'window', 'report', 'server', etc.
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    view_id = Column(Integer, ForeignKey("ir_hr_view.id"))
    report_id = Column(Integer, ForeignKey("ir_hr_report.id"))
    code = Column(Text)  # Python code or reference
