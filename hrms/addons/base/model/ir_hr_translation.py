from sqlalchemy import Column, Integer, String, Text, ForeignKey
from hrms.addons.base.model.base_model import HRMSBase

class IrHrTranslation(HRMSBase):
    __tablename__ = "ir_hr_translation"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    lang = Column(String(10), nullable=False)
    source = Column(Text)
    value = Column(Text)
    res_model = Column(String(128))
    res_id = Column(Integer)
