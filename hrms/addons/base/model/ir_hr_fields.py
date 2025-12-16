from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from hrms.core.utilities.database import Base

class IrHrField(Base):
    __tablename__ = "ir_hr_field"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("ir_hr_model.id"))
    name = Column(String(128), nullable=False)
    field_type = Column(String(64), nullable=False)  # Char, Integer, Many2one, etc.
    string = Column(String(128))                     # Label
    required = Column(Boolean, default=False)
    readonly = Column(Boolean, default=False)
    relation = Column(String(128), nullable=True)    # Related model (for M2x fields)
    help = Column(Text)
