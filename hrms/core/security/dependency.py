# hrms/core/security/dependencies.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from hrms.core.utilities.database import get_db
from hrms.core.security.jwt import decode_access_token, oauth2_scheme
from hrms.addons.base.model.ir_hr_users import User

def require_login(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> User:

    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id), User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
