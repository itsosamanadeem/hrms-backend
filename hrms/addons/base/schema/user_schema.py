from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CreateUserSchema(BaseModel):

    name: str
    email: str
    password: Optional[str] = None

    role : str
    is_super_admin: Optional[bool] = False
    is_active: Optional[bool] = True
    
    model_config = ConfigDict(from_attributes=True)

class ReadUserSchema(BaseModel):
    
    name: str
    email: str
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)