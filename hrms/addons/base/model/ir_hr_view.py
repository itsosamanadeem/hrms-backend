from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from hrms.addons.base.model.base_model import HRMSBase

class IrHrView(HRMSBase):
    __tablename__ = "ir_hr_view"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    view_id = Column(String(128), unique=True, nullable=False)
    name = Column(String(128), nullable=False, unique=True)
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    view_type = Column(String(64))
    xml_data = Column(Text)
    json_data = Column(JSON)

    model = relationship("IrHrModel", back_populates="views")