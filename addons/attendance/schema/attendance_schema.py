from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Optional
from addons.attendance.model.attendance_report import LeaveTypeEnum
# ========================
# Pydantic Schemas
# ========================

class AttendanceCreate(BaseModel):
    employee_id: int
    attendance: Optional[float] = None
    leaves_type: Optional[LeaveTypeEnum] = None


class AttendanceRead(BaseModel):
    id: int
    employee_id: int
    attendance: Optional[float]
    leaves_type: Optional[LeaveTypeEnum]
    employee: Optional["EmployeeLink"] = None

    model_config = ConfigDict(from_attributes=True)


from addons.employees.schema.employee_schema import EmployeeLink