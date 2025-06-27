from typing import List, Dict

from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

from database import get_db_connection
from models.order import Order, OrderItem

from models.product import Product
from schemas.order import AddOrderItem, CreateOrder

db = get_db_connection()


def add_order_item_to_db(item: AddOrderItem, new_order: Order) -> None:
    """
    Adds an order item to the database based on the product and order provided.

    Args:
        item: An object containing product_id and quantity.
        new_order: The order to which this item belongs.

    Raises:
        ValueError: If the product with the given ID is not found.

    Returns:
        None
    """
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


def create_order(order: CreateOrder) -> Order:
    """
    Creates a new order and adds the associated order items to the database.

    Args:
        order: An object with an `items` attribute (list of items with product_id and quantity).

    Raises:
        ValueError: If the order has no items.

    Returns:
        Order: The newly created order instance.
    """
    if len(order.items) == 0:
        raise ValueError("no items in order")

    new_order = Order(user_id=get_jwt_identity())

    db.session.add(new_order)
    db.session.flush()

    for item in order.items:
        add_order_item_to_db(item, new_order)

    db.session.commit()

    return new_order


def get_user_orders(user_id: int) -> List[Dict]:
    """
    Retrieve all orders for a given user by user ID.

    Args:
        user_id (int): The ID of the user whose orders are to be retrieved.

    Returns:
        List[Dict]: A list of dictionaries, each representing an order associated with the user.
                    Each dictionary contains serialized order data via the `to_dict()` method.
    """
    orders = Order.query.filter_by(user_id=user_id).all()
    return [order.to_dict() for order in orders]


def update_quantities(order_items: List[OrderItem]):
    try:
        items = {}
        for item in order_items:
            product = Product.query.filter_by(id=item.product_id).first()
            if product.quantity >= item.quantity:
                product.quantity -= item.quantity
                quantity = item.quantity
            else:
                quantity = product.quantity
                product.quantity = 0

            items[f"{product.name}"] = {"quantity": quantity, "unit_price": product.price}

        db.session.commit()
        return items
    except SQLAlchemyError as e:
        db.session.rollback()
        raise BadRequest("Database error occurred during order execution")


def calculate_order_price(items_dict):
    price = 0.0
    for item in items_dict.values():
        price += item["unit_price"] * item["quantity"]
    return price


def execute_order(order_id: int, user_id: int):
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        raise ValueError(f"no order found with id {order_id}")

    if order.user_id != user_id:
        raise ValueError("User cannot execute orders that do not belong to them.")

    if order.executed:
        raise BadRequest("This order has already been executed.")
    order.executed = True
    db.session.commit()

    order_items = [item for item in order.items]
    final_items = update_quantities(order_items)
    price = calculate_order_price(final_items)

    final_items = list(final_items.items())

    return {"items": final_items, "price": price}
