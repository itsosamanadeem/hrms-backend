from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Optional
from hrms.addons.attendance.model.attendance_report import LeaveTypeEnum
# ========================
# Pydantic Schemas
# ========================

class AttendanceCreate(BaseModel):
    employee_id: int
    attendance: Optional[float] = None
    leaves_type: Optional[LeaveTypeEnum] = None
    attendance_taken: bool = False

class AttendanceRead(BaseModel):
    id: int
    employee_id: int
    attendance: Optional[float]
    leaves_type: Optional[LeaveTypeEnum]
    attendance_taken: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)
