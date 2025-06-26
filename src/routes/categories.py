import http

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from schemas.category import CategoryInfo
from service.db.category_service import get_all_categories, get_products_by_category, update_category_name, \
    delete_category

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('', methods=['GET'])
def handle_get_all_categories():
    try:

        categories = [category.name for category in get_all_categories()]

        return jsonify({"categories": categories}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"errors": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@categories_bp.route('/<category_name>/products', methods=['GET'])
def handle_get_products_by_category(category_name):
    if not category_name:
        return jsonify({"error": " missing 'category' argument ."}), http.HTTPStatus.BAD_REQUEST

    try:
        products = [product.name for product in get_products_by_category(category_name)]
        if products:
            return jsonify({f"{category_name}": products}), http.HTTPStatus.OK

    except Exception as e:
        return jsonify({"errors": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@categories_bp.route('/update', methods=['PUT'])
def handle_update_category_name():
    current_category_name = request.json.get("old_category_name")
    new_category_name = request.json.get("new_category_name")
    if not new_category_name or not current_category_name:
        return jsonify({"error": "missing request arguments."}), http.HTTPStatus.BAD_REQUEST
    try:
        update_category_name(current_category_name, new_category_name)
        return jsonify({"msg": "Category updated successfully."}), http.HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@categories_bp.route('/delete', methods=['DELETE'])
def handle_delete_category():
    category_to_delete = request.json.get("category_to_delete")
    if not category_to_delete:
        return jsonify({"error": "missing request argument."}), http.HTTPStatus.BAD_REQUEST

    try:
        delete_category(category_to_delete)
        return jsonify({"msg": "category was deleted successfully."}), http.HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"error": "couldn't delete category"}), http.HTTPStatus.INTERNAL_SERVER_ERROR
