import http

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from schemas.product import ProductName
from service.product_service import get_product_by_name


product_bp = Blueprint('products', __name__, url_prefix='/products')


@product_bp.route('/name', methods=['GET'])
def handle_get_product_by_name():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "missing name query param"}), http.HTTPStatus.BAD_REQUEST

    return get_product_by_name(name)

