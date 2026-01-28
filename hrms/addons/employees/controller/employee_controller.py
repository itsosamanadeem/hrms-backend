from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.addons.employees.model.hr_employee import HrEmployee
from hrms.addons.employees.schema.employee_schema import EmployeeRead, EmployeeCreate
from hrms.core.security.dependency import require_login
import os
from pathlib import Path

MEDIA_ROOT = Path(os.getenv('MEDIA_DIRECTORY'))
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/employee", tags=["Employee"], dependencies=[Depends(require_login)])

@router.post("/create", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    existing = db.query(HrEmployee).filter((HrEmployee.email == employee.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee with this email or phone already exists.")

    new_employee = HrEmployee(
        emp_name=employee.emp_name,
        email=employee.email,
        phone=employee.phone,
        second_phone=employee.second_phone,
        status=employee.status,
        address=employee.address,
        job_title=employee.job_title,
        dep_name=employee.dep_name,
        employee_type=employee.employee_type,
        employee_group_type=employee.employee_group_type
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee



from fastapi import Request

@router.post("/{employee_id}/upload-image", response_class=JSONResponse)
def upload_employee_image(employee_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), request: Request = None):
    emp = db.query(HrEmployee).filter(HrEmployee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    safe_filename = f"{employee_id}_{file.filename.replace(' ', '_').replace(',', '')}"
    file_location = MEDIA_ROOT / safe_filename

    with file_location.open("wb") as f:
        f.write(file.file.read())

    base_url = str(request.base_url).rstrip("/")
    full_url = f"{base_url}/media/apps/{safe_filename}"

    emp.profile_image = full_url
    db.commit()
    db.refresh(emp)

    return JSONResponse(content={
        "info": "File uploaded successfully",
        "image_url": full_url
    })

@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db), request: Request = None):
    emp = db.query(HrEmployee).filter(HrEmployee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    profile_image_url = f"{emp.profile_image}" if emp.profile_image else None
    return {
        **emp.__dict__,
        "profile_image": profile_image_url
    }


@router.get("", response_model=list[EmployeeRead])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(HrEmployee).offset(skip).limit(limit).all()
    if not employees:
        raise HTTPException(status_code=404, detail="No Employees yet")
    return employees
