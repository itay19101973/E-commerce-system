from datetime import datetime
from database import get_db_connection

db = get_db_connection()


class OrderItem(db.Model):
    """
    Represents an item in an order, linking products to orders.

    Attributes:
        order_id (int): Foreign key to Order, part of composite primary key.
        product_id (int): Foreign key to Product, part of composite primary key.
        quantity (int): Quantity of the product in the order.
        unit_price (float): Price per unit at time of order.
        product (Product): Relationship to the Product model.
    """
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product')


class Order(db.Model):
    """
    Represents a user order.

    Attributes:
        id (int): Primary key.
        created_at (datetime): Timestamp when the order was created.
        items (List[OrderItem]): List of OrderItem instances in this order.
        user_id (int): Foreign key to the User who placed the order.
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan', passive_deletes=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    executed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "executed": self.executed,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in self.items
            ]
        }
