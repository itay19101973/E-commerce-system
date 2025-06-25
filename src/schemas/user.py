from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from typing import Optional


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


class UserUpdateInput(BaseModel):
    id: int
    email: Optional[EmailStr]
    password: Optional[constr(min_length=6)]
    full_name: Optional[str]


class UpdatedUser(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    updated_at: datetime
