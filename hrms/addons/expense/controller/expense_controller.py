from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.core.security import get_current_user
from hrms.addons.expense.model.hrms_expense import Expense
from hrms.addons.expense.schema.expense_schema import ExpenseCreate, ExpenseRead
from hrms.addons.employees.model.hr_employee import HrEmployee

router = APIRouter(prefix="/expense", tags=["Expense"], dependencies=[Depends(get_current_user)])

@router.post("/create", response_model=ExpenseRead)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    # Check if employee exists
    employee = db.query(HrEmployee).filter(HrEmployee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_expense = Expense(
        employee_id=payload.employee_id,
        amount=payload.amount,
        description=payload.description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    exp = db.query(Expense).filter(Expense.expense_id == expense_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return exp


@router.get("", response_model=list[ExpenseRead])
def list_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    expenses = db.query(Expense).offset(skip).limit(limit).all()
    return expenses
