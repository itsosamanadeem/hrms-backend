from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from hrms.core.config import settings
from hrms.core.utilities.database import get_db
from hrms.addons.base.model.ir_hr_users import User
from hrms.core.security.jwt import create_access_token,create_refresh_token,decode_refresh_token
from hrms.core.security.hashing_password import verify_password

router = APIRouter(prefix="/base/auth", tags=["Auth"])

@router.post("/login")
def login(form_data : OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db), responses: Response = None):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    responses.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,          # True in production (HTTPS)
        samesite="lax",    # or "lax" if frontend is separate
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }


@router.post("/refresh")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = decode_refresh_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    new_access_token = create_access_token({"sub": str(user_id)})

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

@router.post('/logout')
def logout(response:Response):
    response.delete_cookie('refresh_token')
    return "logout successfully"