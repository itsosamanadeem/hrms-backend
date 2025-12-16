from sqlalchemy import Column, Integer, String, Text, ForeignKey
from hrms.core.utilities.database import Base

class IrHrView(Base):
    __tablename__ = "ir_hr_view"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    view_id = Column(String(128), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    view_type = Column(String(64))   # form, tree, kanban, dashboard, etc.
    xml_data = Column(Text)          # original XML
    json_data = Column(Text)         # parsed JSON for UI
