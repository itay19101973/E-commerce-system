from datetime import datetime
from typing import List, Dict, Any

from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

from database import get_db_connection
from models.order import Order, OrderItem

from models.product import Product
from schemas.order import AddOrderItem, CreateOrder, OrderItemInfo, OrderInfo, UpdateOrderInput

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


def update_quantities(order: Order) -> None:
    """
    Deducts quantities of products based on the given order's items.

    Args:
        order (Order): The order containing items whose quantities should be updated.

    Raises:
        ValueError: If requested quantity exceeds available product quantity.
        BadRequest: If a database error occurs during update.
    """
    try:
        order_items = [item for item in order.items]
        for item in order_items:
            product = Product.query.filter_by(id=item.product_id).first()
            if product.quantity >= item.quantity:
                product.quantity -= item.quantity
            else:
                raise ValueError(
                    f"cant execute order, asked for {item.quantity} of {product.name} but storage has less.")

        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise BadRequest("Database error occurred during order execution")


def calculate_order_price(order: Order) -> float:
    """
    Calculates the total price for all items in the order.

    Args:
        order (Order): The order whose total price should be calculated.

    Returns:
        float: The total price calculated as sum of (unit_price * quantity) for all items.
    """
    order_items = [item for item in order.items]
    price = 0.0
    for item in order_items:
        price += item.unit_price * item.quantity
    return price


def execute_order(order_id: int, user_id: int) -> Dict[str, Any]:
    """
    Executes an order by validating user ownership, checking execution status,
    updating product quantities, calculating the price, and marking the order as executed.

    Args:
        order_id (int): The ID of the order to execute.
        user_id (int): The ID of the user requesting the execution.

    Returns:
        Dict[str, Any]: A dictionary containing the executed order's item details and total price.

    Raises:
        ValueError: If the order does not exist or does not belong to the user.
        BadRequest: If the order is already executed or a database error occurs.
    """

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        raise ValueError(f"no order found with id {order_id}")

    if order.user_id != user_id:
        raise ValueError("User cannot execute orders that do not belong to them.")

    if order.executed:
        raise BadRequest("This order has already been executed.")
    order.executed = True
    db.session.commit()

    update_quantities(order)
    price = calculate_order_price(order)

    order_items = [item for item in order.items]
    order_details = [{item.product.name: item.quantity} for item in order_items]

    return {"items": order_details, "total_price": price}


def update_order(order_details: UpdateOrderInput, user_id: int) -> OrderInfo:
    """
    Update an existing order's items, replacing them with the given ones.

    Args:
        order_details (UpdateOrder): The order update request, containing id and items.
        user_id (int): The ID of the user attempting the update.

    Returns:
        OrderInfo: The updated order info including order id and list of items.

    Raises:
        BadRequest: If order not found, user mismatch, no items provided, or DB error occurs.
    """
    order = Order.query.filter_by(id=order_details.id).first()
    if not order:
        raise BadRequest(f"There is no order with id {order_details.id}")

    if order.user_id != user_id:
        raise BadRequest("User cannot update orders that do not belong to them.")

    if len(order_details.items) == 0:
        raise BadRequest("No items given to update.")

    if order.executed:
        raise BadRequest("cant update order that already executed.")

    try:

        OrderItem.query.filter_by(order_id=order_details.id).delete()

        for item in order_details.items:
            add_order_item_to_db(item, order)

        db.session.commit()
        updated_items = OrderItem.query.filter_by(order_id=order.id).all()

        updated_items = [
            OrderItemInfo(name=item.product.name, quantity=item.quantity)
            for item in updated_items
        ]
        order.updated_at = datetime.utcnow()

        return OrderInfo(id=order.id, items=updated_items)

    except SQLAlchemyError:
        db.session.rollback()
        raise BadRequest("Database error occurred during order update")


def delete_order(order_id: int, user_id: int) -> None:
    """
    Deletes an existing order if it belongs to the given user.

    Args:
        order_id (int): The ID of the order to delete.
        user_id (int): The ID of the user requesting the deletion.

    Raises:
        BadRequest: If the order does not exist or the user is not the owner.

    Behavior:
        - If the order exists and belongs to the user, it is removed from the database.
        - Commits the transaction to persist the deletion.
    """
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        raise BadRequest(f"There is no order with id {order_id}")

    if order.user_id != user_id:
        raise BadRequest("User cannot delete orders that do not belong to them.")

    db.session.delete(order)
    db.session.commit()

