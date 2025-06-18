import http

from flask import jsonify

from schemas.product import ProductInfo
from schemas.user import UserInfo

from models.product import Product


def get_product_by_name(product_name):
    product = Product.query.filter_by(name=product_name).first()

    if not product:
        return jsonify({"error_msg": "Product doesn't exist"}), http.HTTPStatus.NOT_FOUND

    return jsonify(ProductInfo.from_orm(product).dict()), http.HTTPStatus.OK
