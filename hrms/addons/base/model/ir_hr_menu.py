from sqlalchemy import Column, Integer, String, ForeignKey
from hrms.core.utilities.database import Base

class IrHrMenu(Base):
    __tablename__ = "ir_hr_menu"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    parent_id = Column(Integer, ForeignKey("ir_hr_menu.id"), nullable=True)
    sequence = Column(Integer, default=10)
    action_model = Column(String(128), nullable=True)
    action_view_id = Column(Integer, ForeignKey("ir_hr_view.id"), nullable=True)
