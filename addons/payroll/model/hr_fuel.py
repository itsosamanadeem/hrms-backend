from sqlalchemy import Integer, String, Column, ForeignKey, Double
from core.utilities.database import Base
class HrFuel(Base):
    __tablename__ = "hr_fuel"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('hr_employee.id'))
    fuel_amount = Column(Double, default=0.0)