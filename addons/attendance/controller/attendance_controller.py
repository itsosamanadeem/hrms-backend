from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.utilities.database import get_db
from addons.attendance.model.attendance_report import IrHrAttendance
from addons.employees.model.hr_employee import HrEmployee
from addons.attendance.schema.attendance_schema import AttendanceCreate, AttendanceRead
router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/create", response_model=AttendanceRead)
def create_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):

    # Validate employee exists
    employee = db.query(HrEmployee).filter(HrEmployee.id == data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance = IrHrAttendance(
        employee_id=data.employee_id,
        attendance=data.attendance,
        leaves_type=data.leaves_type,
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


@router.get("/{attendance_id}", response_model=AttendanceRead)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(IrHrAttendance).filter(IrHrAttendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return record

@router.get("/", response_model=list[AttendanceRead])
def list_attendance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(IrHrAttendance).offset(skip).limit(limit).all()
    return records

@router.get("/employee/{employee_id}", response_model=list[AttendanceRead])
def get_attendance_by_employee(employee_id: int, db: Session = Depends(get_db)):
    data = db.query(IrHrAttendance).filter(IrHrAttendance.employee_id == employee_id).all()

    if not data:
        raise HTTPException(status_code=404, detail="No attendance records found for this employee")

    return data

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(IrHrAttendance).filter(IrHrAttendance.id == attendance_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    db.delete(record)
    db.commit()
    return {"detail": "Attendance record deleted"}