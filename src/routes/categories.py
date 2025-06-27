import http

from flask import Blueprint, request, jsonify
from service.db.category_service import get_all_categories, get_products_by_category, update_category_name, \
    delete_category

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('', methods=['GET'])
def handle_get_all_categories():
    """
    Get a list of all category names.

    Returns:
        JSON with list of category names and HTTP 200 status,
        or HTTP 500 on failure.
    """
    try:

        categories = [category.name for category in get_all_categories()]

        return jsonify({"categories": categories}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"errors": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@categories_bp.route('/<category_name>/products', methods=['GET'])
def handle_get_products_by_category(category_name):
    """
    Get all product names belonging to a given category.

    Args:
        category_name (str): Provided via URL path parameter.

    Returns:
        - HTTP 200 OK:
            {
                "<category_name>": [<product_name>, ...]
            }
        - HTTP 400 Bad Request:
            {
                "error": "missing 'category' argument."
            }
        - HTTP 500 Internal Server Error:
            {
                "errors": "<error_message>"
            }
    """
    if not category_name:

        return jsonify({"error": " missing 'category' argument ."}), http.HTTPStatus.BAD_REQUEST

    try:
        products = get_products_by_category(category_name)
        if products:
            return jsonify({f"{category_name}": products}), http.HTTPStatus.OK

    except Exception as e:
        return jsonify({"errors": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@categories_bp.route('/update', methods=['PUT'])
def handle_update_category_name():
    """
    Update a category name.

    Expects JSON with keys:
        - old_category_name: str
        - new_category_name: str

    Returns:
        Success message with HTTP 200,
        or HTTP 400 if arguments are missing,
        or HTTP 404 if category not found,
        or HTTP 500 on failure.
    """
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
    """
    Delete a category.

    Expects JSON with key:
        - category_to_delete: str

    Returns:
        Success message with HTTP 200,
        or HTTP 400 if argument is missing,
        or HTTP 404 if category not found,
        or HTTP 500 on failure.
    """
    category_to_delete = request.json.get("category_to_delete")
    if not category_to_delete:
        return jsonify({"error": "missing request argument."}), http.HTTPStatus.BAD_REQUEST

    try:
        delete_category(category_to_delete)
        return jsonify({"msg": "category was deleted successfully."}), http.HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.NOT_FOUND
    except Exception:
        return jsonify({"error": "couldn't delete category"}), http.HTTPStatus.INTERNAL_SERVER_ERROR
