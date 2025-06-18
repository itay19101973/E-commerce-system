
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from schemas.user import UserRegistration, UserInfo, UserLoginRequest
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from service.user_service import create_user, login_user
from utils.authentication import revoke_jwt_token

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
def handle_create_user():
    try:
        user_data = UserRegistration(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    return create_user(user_data)


@users_bp.route('/login', methods=['POST'])
def handle_user_login():
    try:
        login_data = UserLoginRequest(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    return login_user(login_data)


# For maintaining the session while surfing the app
@users_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_user_token():
    current_user_id = str(get_jwt_identity())
    print(current_user_id)
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200


@users_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def handle_user_logout():
    revoke_jwt_token()
    return jsonify({"msg": "Refresh token revoked, logged out"}), 200
