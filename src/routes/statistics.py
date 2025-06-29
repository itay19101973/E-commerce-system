import http

from flask import Blueprint, jsonify

from service.db.order_service import calculate_total_order_sales
from service.db.statistics import calculate_product_sales_percentage, calculate_category_product_sales

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_bp.route('/profit', methods=['GET'])
def handle_get_total_profit():
    """
    GET /profit

    Calculates and returns the total profit from all executed orders.

    Returns:
        JSON response with:
            - number_of_executed_orders: int
            - total_profit: float

    Response Codes:
        200 OK: Successfully calculated and returned sales info.
        500 Internal Server Error: If an exception occurs during processing.
    """
    try:
        sales = calculate_total_order_sales()
        return jsonify(sales.dict()), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@statistics_bp.route('/product-sales', methods=['GET'])
def get_product_sales():
    """
    Returns sales percentage of each product across all **executed** orders.
    """
    try:
        results = calculate_product_sales_percentage()
        return jsonify([r.dict() for r in results]), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@statistics_bp.route('/category-product-sales', methods=['GET'])
def get_category_product_sales():
    """
    Returns product sales percentages grouped by category from executed orders.
    """
    try:
        results = calculate_category_product_sales()
        return jsonify([r.dict() for r in results]), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR
