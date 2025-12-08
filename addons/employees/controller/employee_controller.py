from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.addons.employees.model.hr_employee import HrEmployee
from hrms.addons.employees.schema.employee_schema import EmployeeRead, EmployeeCreate

router = APIRouter(prefix="/employee", tags=["Employee"])

# ==========================
# Routes
# ==========================

@router.post("/create", response_model=EmployeeRead)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Check for duplicate email or phone
    existing = db.query(HrEmployee).filter(
        (HrEmployee.email == employee.email) |
        (HrEmployee.phone == employee.phone) |
        (HrEmployee.second_phone == employee.second_phone)
    ).first()
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


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(HrEmployee).filter(HrEmployee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.get("", response_model=list[EmployeeRead])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(HrEmployee).offset(skip).limit(limit).all()
    if not employees:
        raise HTTPException(status_code="404", detail="No Employees yet")
    return employees
