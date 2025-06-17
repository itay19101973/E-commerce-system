from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserRegistration(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    full_name: str

class UserInfo(BaseModel):
    id: int
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

