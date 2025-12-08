from sqlalchemy import Column, Integer, String, Text
from hrms.core.utilities.database import Base
from sqlalchemy.orm import mapped_column, Mapped

class IrHrSetting(Base):
    __tablename__ = "ir_hr_setting"
    __table_args__ = {"extend_existing": True}


    id: Mapped[int] = mapped_column(String(128), primary_key=True)
    # id = Column(Integer, primary_key=True)
    # key = Column(String(128), unique=True)
    # value = Column(Text)
