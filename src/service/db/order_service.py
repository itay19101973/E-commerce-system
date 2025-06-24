from flask import jsonify

from database import get_db_connection
from models.category import Category
from models.order import Order, OrderItem

from models.product import Product

db = get_db_connection()


def add_order_item_to_db(item, new_order):
    product = Product.query.get(item.product_id)
    if not product:
        raise ValueError(f"Product with ID {item.product_id} not found")

    order_item = OrderItem(
        order_id=new_order.id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=product.price
    )
    db.session.add(order_item)


def create_order(order):
    if len(order.items) == 0:
        raise ValueError("no items in order")

    new_order = Order(user_id=order.user_id)

    db.session.add(new_order)
    db.session.flush()

    for item in order.items:
        add_order_item_to_db(item, new_order)

    db.session.commit()

    return new_order

