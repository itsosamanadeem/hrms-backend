from sqlalchemy import Column, Integer,ForeignKey
from core.utilities.database import Base

class Expense(Base):

    __tablename__ = "hr_expense"
    __table_args__ = {"extend_existing": True}

    expense_id = Column(Integer, primary_key=True)