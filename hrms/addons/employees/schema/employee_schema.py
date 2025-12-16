from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from hrms.addons.employees.model.hr_employee import EmpTypeEnum, EmpGroupLevel
from hrms.addons.expense.schema.expense_schema import ExpenseRead
from hrms.addons.attendance.schema.attendance_schema import AttendanceRead

# ==========================
# Pydantic schemas
# ==========================

class EmployeeLink(BaseModel):
    emp_name: str
    email: EmailStr
    phone: str

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(BaseModel):
    emp_name: str
    email: EmailStr
    phone: str
    second_phone: str | None = None
    status: Optional[str] = "draft"
    address: str | None = None
    job_title: str | None = None
    dep_name: str | None = None
    employee_type: EmpTypeEnum | None = None
    employee_group_type: EmpGroupLevel | None = None

class EmployeeRead(BaseModel):
    id: int
    emp_name: str
    email: EmailStr
    phone: str
    second_phone: str | None
    status: Optional[str]
    address: str | None
    job_title: str | None
    dep_name: str | None
    employee_type: EmpTypeEnum | None
    employee_group_type: EmpGroupLevel | None
    expense: list[ExpenseRead] = []
    attendance_ids: list[AttendanceRead] = []

    class Config:
        from_attributes = True

