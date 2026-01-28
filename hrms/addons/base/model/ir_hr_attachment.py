from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from hrms.addons.base.model.base_model import HRMSBase

class IrHrAttachment(HRMSBase):
    __tablename__ = "ir_hr_attachment"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    res_model = Column(String(128))
    res_id = Column(Integer)
    file_name = Column(String(256))
    data = Column(LargeBinary)
