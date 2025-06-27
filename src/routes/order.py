import http

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from schemas.order import CreateOrder, ExecuteOrder, UpdateOrderInput
from service.db.order_service import create_order, get_user_orders, execute_order, update_order

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['POST'])
@jwt_required()
def handle_create_order():
    """
    Handle order creation request.

    Parses and validates the incoming JSON request using the CreateOrder schema.
    Then creates the order in the database.

    Returns:
        - HTTP 201 with the created order ID on success.
        - HTTP 400 with validation error details on failure.
    """
    try:
        order = CreateOrder(**request.json)
        new_order = create_order(order)
        return jsonify({"id": new_order.id}), http.HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), http.HTTPStatus.BAD_REQUEST


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def handle_get_user_order():
    """
    Handle GET request to retrieve all orders for the authenticated user.

    Requires:
        A valid JWT token in the Authorization header.

    Returns:
        JSON response containing:
            - "user": The authenticated user's ID.
            - "orders": A list of the user's orders in dictionary format.
        HTTP 200 OK on success.

    Error Handling:
        Returns JSON error message with a generic failure note if an exception occurs.
    """
    user_id = get_jwt_identity()
    try:
        orders = get_user_orders(user_id)
        return jsonify({"user": f"{user_id}", "orders": orders}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": f"failed to get orders for user {user_id}"})


@orders_bp.route('/execute', methods=['POST'])
@jwt_required()
def handle_execute_order():
    user_id = int(get_jwt_identity())
    try:
        order = ExecuteOrder(**request.json)
        order_id = order.id
        order_details = execute_order(order_id, user_id)
        return (jsonify({"msg": f"order {order_id} executed successfully.", "details": f"{order_details}"}),
                http.HTTPStatus.OK)
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), http.HTTPStatus.BAD_REQUEST
    except BadRequest as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": "cant execute order, try again later."}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@orders_bp.route('/update', methods=['POST'])
@jwt_required()
def handle_update_order():
    try:
        order_details = UpdateOrderInput(**request.json)
        user_id = int(get_jwt_identity())
        order_info = update_order(order_details, user_id)
        return (jsonify({"msg": f"order {order_details.id} updated successfully.", "details": order_info.dict()}),
                http.HTTPStatus.OK)
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), http.HTTPStatus.BAD_REQUEST
    except BadRequest as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR
