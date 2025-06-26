
from typing import Any, Dict, Optional


from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection
from models.user import User
from schemas.user import UserInfo, UpdatedUser, UserRegistration, UserLoginRequest, UserUpdateInput

db = get_db_connection()


def create_user(user_data: UserRegistration) -> UserInfo:
    """
    Create a new user in the database.

    Args:
        user_data: Pydantic model containing user registration data
                   (with attributes: email, password, full_name).

    Raises:
        ValueError: If a user with the given email already exists.

    Returns:
        UserInfo: The created user info as a Pydantic model.
    """
    exist_user = User.query.filter_by(email=user_data.email).first()
    if exist_user:
        raise ValueError("user with given email already exist.")

    user = User(
        email=user_data.email,
        password_hash=generate_password_hash(user_data.password),
        full_name=user_data.full_name
    )

    db.session.add(user)
    db.session.commit()
    return UserInfo.from_orm(user)


def login_user(login_data: UserLoginRequest) -> Dict[str, str]:
    """
       Verify user credentials and generate JWT access and refresh tokens.

       Args:
           login_data: Pydantic model containing user login data
                       (with attributes: email, password).

       Raises:
           ValueError: If email or password is invalid.

       Returns:
           dict: Contains 'access_token' and 'refresh_token' strings.
    """
    user = User.query.filter_by(email=login_data.email).first()

    if not user or not check_password_hash(user.password_hash, login_data.password):
        raise ValueError("Invalid email or password")

    # for session managment
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def find_user_by_id(user_id: int) -> Optional[User]:
    """
      Find a user by their ID.

      Args:
          user_id: The user ID to query.

      Returns:
          Optional[User]: The User object if found, else None.
    """
    return User.query.filter_by(id=user_id).first()


def update_user(input_data: UserUpdateInput) -> UpdatedUser:
    """
    Update user information.

    Args:
        input_data: Pydantic model with user update data
                    (must include id, optionally email, password, full_name).

    Raises:
        ValueError: If user is not found.

    Returns:
        UpdatedUser: Pydantic model of updated user information.
    """
    user = find_user_by_id(input_data.id)
    if not user:
        raise ValueError("User not found")

    if input_data.email:
        user.email = input_data.email

    if input_data.password:
        user.password_hash = generate_password_hash(input_data.password)

    if input_data.full_name:
        user.full_name = input_data.full_name

    db.session.commit()

    return UpdatedUser(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        updated_at=user.updated_at
    )


def delete_user(user_id: int) -> None:
    """
    Delete a user by their ID.

    Args:
        user_id: The user ID to delete.

    Returns:
        None
    """
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        raise ValueError("user to delete wasn't found.")
