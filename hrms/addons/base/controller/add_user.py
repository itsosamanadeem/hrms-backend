from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.addons.base.schema.user_schema import CreateUserSchema, ReadUserSchema
from hrms.addons.base.model.ir_hr_users import User
from hrms.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", response_model=CreateUserSchema)
def add_user(user_data: CreateUserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=ReadUserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user