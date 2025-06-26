from datetime import datetime
from database import get_db_connection

db = get_db_connection()


class Product(db.Model):
    """
    Represents a product in the inventory.

    Attributes:
        id (int): Primary key.
        name (str): Unique product name.
        quantity (int): Available quantity.
        price (int): Price of the product.
        category_id (int): Foreign key to Category.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last updated timestamp.
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # relations
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "category": self.category.name if self.category else None
        }
