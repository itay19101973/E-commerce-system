
from typing import List

from models.order import Order, OrderItem
from models.product import Product
from models.category import Category
from schemas.statistics import ProductSalesPercentage, CategoryProductSales, ProductSalesInCategory
from sqlalchemy.orm import joinedload
from database import get_db_connection
from collections import defaultdict

db = get_db_connection()


def calculate_product_sales_percentage() -> List[ProductSalesPercentage]:
    """
    Calculate the overall percentage of total sales for each product across all executed orders.

    Returns:
        List[ProductSalesPercentage]: A list of products with their total quantity sold
        and the percentage they represent from the overall sold items.
    """
    executed_orders = Order.query.options(joinedload(Order.items)).filter_by(executed=True).all()

    product_sales = defaultdict(int)
    total_quantity = 0

    for order in executed_orders:
        for item in order.items:
            product_sales[item.product_id] += item.quantity
            total_quantity += item.quantity

    results = []
    for product_id, qty in product_sales.items():
        product = Product.query.get(product_id)
        percentage = (qty / total_quantity * 100) if total_quantity > 0 else 0
        results.append(ProductSalesPercentage(
            product_id=product.id,
            product_name=product.name,
            total_quantity_sold=qty,
            sales_percentage=round(percentage, 2)
        ))

    return results


def calculate_category_product_sales() -> List[CategoryProductSales]:
    """
    Calculate the sales statistics per category, showing how much each product
    contributes to its own category's total sales.

    Returns:
        List[CategoryProductSales]: A list where each entry contains a category,
        its total quantity sold, and the list of products with their quantity
        and percentage within that category.
    """
    executed_orders = Order.query.options(joinedload(Order.items)).filter_by(executed=True).all()

    category_sales = defaultdict(lambda: defaultdict(int))
    product_info = {}

    for order in executed_orders:
        for item in order.items:
            product = Product.query.get(item.product_id)
            product_info[product.id] = product
            category_sales[product.category_id][product.id] += item.quantity

    category_results = []
    for category_id, products in category_sales.items():
        category = Category.query.get(category_id)
        total_category_qty = sum(products.values())

        product_data = []
        for pid, qty in products.items():
            product = product_info[pid]
            percentage = (qty / total_category_qty * 100) if total_category_qty > 0 else 0
            product_data.append(ProductSalesInCategory(
                product_id=product.id,
                product_name=product.name,
                quantity_sold=qty,
                sales_percentage_within_category=round(percentage, 2)
            ))

        category_results.append(CategoryProductSales(
            category_id=category.id,
            category_name=category.name,
            total_category_quantity=total_category_qty,
            products=product_data
        ))

    return category_results
