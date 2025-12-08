from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from hrms.core.utilities.database import Base

class User(Base):
    __tablename__ = "ir_hr_users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    group_id = Column(Integer, ForeignKey("ir_hr_group.id"))
    group = relationship("IrHrGroup")
