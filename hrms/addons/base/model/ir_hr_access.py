from sqlalchemy import Column, Integer, ForeignKey, Boolean
from hrms.core.utilities.database import Base

class IrHrAccess(Base):
    __tablename__ = "ir_hr_access"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    group_id = Column(Integer, ForeignKey("ir_hr_group.id"))
    perm_read = Column(Boolean, default=True)
    perm_write = Column(Boolean, default=False)
    perm_create = Column(Boolean, default=False)
    perm_unlink = Column(Boolean, default=False)
