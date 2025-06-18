import http

from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_db_connection
from models.user import User
from schemas.user import UserInfo


def create_user(user_data):
    user = User(
        email=user_data.email,
        password_hash=generate_password_hash(user_data.password),
        full_name=user_data.full_name
    )
    try:
        db = get_db_connection()
        db.session.add(user)
        db.session.commit()
        return jsonify(UserInfo.from_orm(user).dict()), http.HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error_msg": "couldn't add user to the database"}), http.HTTPStatus.INTERNAL_SERVER_ERROR


def login_user(login_data):
    user = User.query.filter_by(email=login_data.email).first()

    if not user or not check_password_hash(user.password_hash, login_data.password):
        return jsonify({"error": "Invalid email or password"}), http.HTTPStatus.UNAUTHORIZED

    # for session managment
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), http.HTTPStatus.OK




