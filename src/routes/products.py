import http

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from schemas.product import ProductInfo, UpdateProduct
from service.db.category_service import get_category_name_by_id
from service.db.product_service import get_product_by_name, add_product_to_db, remove_product, update_product

product_bp = Blueprint('products', __name__, url_prefix='/products')


@product_bp.route('/', methods=['GET'])
def handle_get_product_info_by_name():
    """
    Handle request to get product information by name.

    Returns:
        JSON response with product info or error message.
    """
    try:

        name = request.args.get("name")
        if not name:
            return jsonify({"error": "missing name query param"}), http.HTTPStatus.BAD_REQUEST
        product = get_product_by_name(name)
        category_name = get_category_name_by_id(product.id)
        return jsonify(ProductInfo(id=product.id, name=product.name, quantity=product.quantity,
                                   category=category_name, price=product.price).dict()), http.HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception:
        return jsonify(
            {"error": "couldn't get the product info due to an internal error."}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@product_bp.route('/add', methods=['POST'])
def handle_add_product():
    """
    Handle request to add a new product.

    Expects:
        JSON body conforming to ProductInfo schema:
        {
            "id": int,
            "name": str,
            "quantity": int,
            "category": str,
            "price": int
        }

    Returns:
        - HTTP 201 Created:
            {
                "id": <new_product_id>
            }
        - HTTP 400 Bad Request:
            {
                "error": <validation_errors>
            }
    """
    try:
        product_data = ProductInfo(**request.json)
        return jsonify({"id": add_product_to_db(**product_data.dict()).id}), http.HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"error": e.errors()}), http.HTTPStatus.BAD_REQUEST


@product_bp.route('/remove', methods=['DELETE'])
def handle_remove_product_by_id():
    """
    Handle request to remove a product by ID.

    Expects:
        Query parameter:
            /remove?id=<product_id>

    Returns:
        - HTTP 200 OK:
            {
                "msg": "product deleted",
                "success": true
            }
        - HTTP 400 Bad Request:
            {
                "error": "Invalid or missing 'id' parameter"
            }
    """
    product_id = request.args.get("id")

    # Check for missing or non-integer value
    if not product_id or not product_id.isdigit():
        return jsonify({"error": f"Invalid or missing 'id' parameter: {product_id}"}), http.HTTPStatus.BAD_REQUEST

    product_id = int(product_id)

    try:
        remove_product(product_id)
        return jsonify({"msg": "product deleted", "success": True}), http.HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST


@product_bp.route('/update', methods=['PUT'])
def handle_update_product_details():
    """
    Handle request to update product details.

    Expects:
        JSON body conforming to UpdateProduct schema:
        {
            "id": int,
            "name": Optional[str],
            "quantity": Optional[int],
            "category": Optional[str],
            "price": Optional[int]
        }

        At least one of the fields (name, quantity, category, price) must be provided.

    Returns:
        - HTTP 200 OK:
            {
                "id": int,
                "name": str,
                "quantity": int,
                "category": str,
                "price": int
            }
        - HTTP 400 Bad Request:
            {
                "error": <validation or logic error>
            }
        - HTTP 500 Internal Server Error:
            {
                "error": "couldn't update product."
            }
    """
    try:
        new_product_details = UpdateProduct(**request.json)
        if not any([new_product_details.name,
                    new_product_details.quantity,
                    new_product_details.category,
                    new_product_details.price]):
            return jsonify({"msg": "nothing to change."}), http.HTTPStatus.OK

        new_product = update_product(new_product_details)

        return jsonify(new_product.to_dict()), http.HTTPStatus.OK

    except ValidationError as e:
        return jsonify({"error": e.errors()}), http.HTTPStatus.BAD_REQUEST
    except ValueError as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.BAD_REQUEST
    except Exception:
        return jsonify({"error": "couldn't update product."}), http.HTTPStatus.INTERNAL_SERVER_ERROR
