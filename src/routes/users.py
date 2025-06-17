from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from schemas.user import UserRegistration, UserInfo, UserLoginRequest
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

@users_bp.route('/login', methods=['POST'])
def login_user():
    try:
        login_data = UserLoginRequest(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    user = User.query.filter_by(email=login_data.email).first()

    if not user or not check_password_hash(user.password_hash, login_data.password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify(UserInfo.from_orm(user).dict()), 200