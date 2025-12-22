from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CreateUserSchema(BaseModel):

    name: str
    email: EmailStr
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ReadUserSchema(BaseModel):
    
    name: str
    email: str
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)