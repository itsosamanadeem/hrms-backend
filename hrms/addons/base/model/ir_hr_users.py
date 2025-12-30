from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from hrms.core.utilities.database import Base

class User(Base):
    __tablename__ = "ir_hr_users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    role = Column(String, nullable=False)
    is_super_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    must_change_password = Column(Boolean,default=False)
    must_change_email = Column(Boolean,default=False)

    group_id = Column(Integer, ForeignKey("ir_hr_group.id"))
    group = relationship("IrHrGroup")
