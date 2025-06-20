import http

from flask import Blueprint, request, jsonify

from schemas.product import ProductInfo
from service.db.category_service import get_category_name_by_id
from service.db.product_service import get_product_by_name

product_bp = Blueprint('products', __name__, url_prefix='/products')


@product_bp.route('/', methods=['GET'])
def handle_get_product_info_by_name():
    try:

        name = request.args.get("name")
        if not name:
            return jsonify({"error": "missing name query param"}), http.HTTPStatus.BAD_REQUEST
        product = get_product_by_name(name)
        category_name = get_category_name_by_id(product.id)
        return jsonify(ProductInfo(name=product.name, quantity=product.quantity, category=category_name).dict()), http.HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify(
            {"error": "couldn't get the product info due to an internal error."}), http.HTTPStatus.INTERNAL_SERVER_ERROR
