import http

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from schemas.user import UserRegistration, UserLoginRequest, UserUpdateInput
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from service.db.user_service import create_user, login_user, update_user, delete_user
from utils.authentication import revoke_jwt_token

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/add', methods=['POST'])
def handle_create_user():
    try:
        user_data = UserRegistration(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), http.HTTPStatus.BAD_REQUEST

    return create_user(user_data)


@users_bp.route('/login', methods=['POST'])
def handle_user_login():
    try:
        login_data = UserLoginRequest(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), http.HTTPStatus.BAD_REQUEST

    return login_user(login_data)


# For maintaining the session while surfing the app
@users_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_user_token():
    current_user_id = str(get_jwt_identity())
    print(current_user_id)
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), http.HTTPStatus.OK


@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def handle_user_logout():
    revoke_jwt_token()
    return jsonify({"msg": "Refresh token revoked, logged out"}), http.HTTPStatus.OK


@users_bp.route('/update', methods=['PUT'])
def handle_update_user():
    try:
        input_data = UserUpdateInput(**request.json)
        updated_user = update_user(input_data)
        return jsonify(updated_user.dict()), http.HTTPStatus.OK

    except ValidationError as ve:
        return jsonify({"error":  ve.errors()}), http.HTTPStatus.BAD_REQUEST

    except ValueError as ve:
        return jsonify({"error": str(ve)}), http.HTTPStatus.NOT_FOUND

    except Exception:
        return jsonify({"error": "Failed to update user"}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@users_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def handle_delete_user():
    user_id = get_jwt_identity()
    try:
        delete_user(user_id)
        return jsonify({"msg": "user deleted successfully."}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": f"couldn't delete user {user_id}."}), http.HTTPStatus.INTERNAL_SERVER_ERROR





