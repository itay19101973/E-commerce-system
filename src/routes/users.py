from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.user import User
from schemas.user import UserRegistration, UserInfo
from db import get_db_connection
from pydantic import ValidationError

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('', methods=['POST'])
def create_user():
    try:
        user_data = UserRegistration(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    user = User(
        email=user_data.email,
        password_hash=generate_password_hash(user_data.password),
        full_name=user_data.full_name
    )

    db = get_db_connection()
    db.session.add(user)
    db.session.commit()

    return jsonify(UserInfo.from_orm(user).dict()), 201