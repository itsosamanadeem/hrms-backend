from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ExpenseCreate(BaseModel):
    employee_id: int = Field(..., description="ID of the employee submitting the expense")
    amount: float = Field(..., description="Expense amount")
    description: str = Field(..., description="Description of the expense")

class ExpenseRead(BaseModel):
    expense_id: int
    employee_id: int
    amount: float
    description: str

    model_config = ConfigDict(from_attributes=True)
