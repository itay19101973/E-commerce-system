import http

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from schemas.category import CategoryInfo
from service.db.category_service import get_all_categories

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('', methods=['GET'])
def handle_get_all_categories():
    try:

        categories = [category.name for category in get_all_categories()]

        return jsonify({"categories": categories}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"errors": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR

