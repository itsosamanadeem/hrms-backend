from sqlalchemy import Column, String, Integer,ForeignKey
from hrms.core.utilities.database import Base

class TimeSheet(Base):

    __tablename__ = 'hr_timesheet'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('hr_employee.id'))
