import http

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from schemas.order import CreateOrder, ExecuteOrder, UpdateOrderInput, DeleteOrderInput
from service.db.order_service import create_order, get_user_orders, execute_order, update_order, delete_order

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['POST'])
@jwt_required()
def handle_create_order():
    """
    Create a new order for the authenticated user.

    Expects:
        JSON payload matching the CreateOrder schema:
        {
            "user_id": int,
            "items": [
                {
                    "product_id": int,
                    "quantity": int
                },
                ...
            ]
        }

    Requires:
        - A valid JWT token in the Authorization header.

    Returns:
        - HTTP 201 Created:
            {
                "id": <new_order_id>
            }
        - HTTP 400 Bad Request:
            {
                "errors": <validation_errors>
            }
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
    Retrieve all orders for the authenticated user.

    Requires:
        - A valid JWT token in the Authorization header.

    Returns:
        - HTTP 200 OK:
            {
                "user": "<user_id>",
                "orders": [
                    {
                        "id": int,
                        "created_at": str (ISO 8601 datetime),
                        "executed": bool,
                        "items": [
                            {
                                "product_id": int,
                                "product_name": str,
                                "quantity": int,
                                "unit_price": float
                            },
                            ...
                        ]
                    },
                    ...
                ]
            }

        - HTTP 500 Internal Server Error:
            {
                "error": "failed to get orders for user <user_id>"
            }
    """
    user_id = get_jwt_identity()
    try:
        orders = get_user_orders(user_id)
        return jsonify({"user": f"{user_id}", "orders": orders}), http.HTTPStatus.OK
    except Exception:
        return jsonify({"error": f"failed to get orders for user {user_id}"})


@orders_bp.route('/execute', methods=['POST'])
@jwt_required()
def handle_execute_order():
    """
    Executes a given order for the authenticated user.

    Expects:
        JSON payload with the order ID:
        {
            "id": <order_id: int>
        }

    Requires:
        JWT-authenticated user.

    Returns:
        200 OK: If the order is successfully executed.
        400 Bad Request: If the order is not found, not owned by the user, already executed, or database error.
        422 Unprocessable Entity: If input validation fails.
        500 Internal Server Error: On unexpected errors.
    """
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
    except Exception:
        return jsonify({"error": "cant execute order, try again later."}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@orders_bp.route('/update', methods=['POST'])
@jwt_required()
def handle_update_order():
    """
    Updates an existing order with new items for the authenticated user.

    Expects:
        JSON payload with order ID and list of new items:
        {
            "id": <order_id: int>,
            "items": [{"product_id": int, "quantity": int}, ...]
        }

    Requires:
        JWT-authenticated user.

    Returns:
        200 OK: If the order is successfully updated.
        400 Bad Request: If validation fails or order is invalid.
        500 Internal Server Error: On unexpected errors.
    """
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


@orders_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def handle_delete_order():
    """
    Deletes an order by ID for the authenticated user.

    Expects:
        JSON payload with the order ID:
        {
            "id": <order_id: int>
        }

    Requires:
        JWT-authenticated user.

    Returns:
        200 OK: If the order is successfully deleted.
        400 Bad Request: If validation fails or deletion is not allowed.
        500 Internal Server Error: On unexpected errors.
    """
    try:
        order_id = DeleteOrderInput(**request.json).id
        user_id = int(get_jwt_identity())
        delete_order(order_id, user_id)
        return jsonify({"msg": f"order {order_id} deleted successfully."}), http.HTTPStatus.OK

    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), http.HTTPStatus.BAD_REQUEST
    except BadRequest as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR
