from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional


class UserRegistration(BaseModel):
    """
    Schema for user registration input.

    Attributes:
        email: A valid email address.
        password: A password string with at least 6 characters.
        full_name: The full name of the user.
    """
    email: EmailStr
    password: constr(min_length=6)
    full_name: str


class UserInfo(BaseModel):
    """
    Schema for returning basic user information.

    Attributes:
        id: The user's unique identifier.
        full_name: The full name of the user.
        created_at: The timestamp when the user was created.
    """
    id: int
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True


class UserLoginRequest(BaseModel):
    """
    Schema for user login input.

    Attributes:
        email: The email address used for login.
        password: The password used for login (minimum 6 characters).
    """
    email: EmailStr
    password: constr(min_length=6)


class UserUpdateInput(BaseModel):
    """
    Schema for updating user information.

    Attributes:
        id: The ID of the user to update.
        email: Optional new email address.
        password: Optional new password (minimum 6 characters).
        full_name: Optional new full name.
    """
    id: int
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None
    full_name: Optional[str] = None


class UpdatedUser(BaseModel):
    """
    Schema returned after a user is updated.

    Attributes:
        id: The updated user's ID.
        full_name: The updated full name.
        email: The updated email address.
        updated_at: Timestamp of the update.
    """
    id: int
    full_name: str
    email: EmailStr
    updated_at: datetime
