from sqlalchemy import Column, String, Integer,ForeignKey
from hrms.addons.base.model.base_model import HRMSBase

class TimeSheet(HRMSBase):

    __tablename__ = 'hr_timesheet'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('hr_employee.id'))
