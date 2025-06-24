import http

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from schemas.order import CreateOrder
from service.db.order_service import create_order

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['POST'])
def handle_create_order():
    try:
        order = CreateOrder(**request.json)
        new_order = create_order(order)
        return jsonify({"id": new_order.id}), http.HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), http.HTTPStatus.BAD_REQUEST





