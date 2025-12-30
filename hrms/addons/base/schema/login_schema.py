# from pydantic import BaseModel, EmailStr, Field, field_validator

# class LoginSchema(BaseModel):
#     email: str = Field(..., description="The email address of the user")
#     password: str = Field(..., description="The password of the user")

#     @field_validator('email')
#     def validate_email(cls, v):
#         if not isinstance(v, str) or '@' not in v:
#             raise ValueError('Invalid email address')
#         return v