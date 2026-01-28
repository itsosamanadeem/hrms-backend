from sqlalchemy import Integer, String, Column, ForeignKey, Double,Enum
from hrms.addons.base.model.base_model import HRMSBase

fuel_type_enum = Enum('petrol', 'cng', name='fuel_type', create_type=True)

class HrFuel(HRMSBase):
    __tablename__ = "hr_fuel"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('hr_employee.id'))
    fuel_amount = Column(Double, default=0.0)
    fuel_type = Column(fuel_type_enum, nullable=True)