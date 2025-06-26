from datetime import datetime
from database import get_db_connection

db = get_db_connection()


class Category(db.Model):
    """
    Represents a product category.

    Attributes:
        id (int): Primary key identifier for the category.
        name (str): Unique name of the category.
        products (List[Product]): List of associated Product objects.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # One-to-many relationship (one category → many products)
    products = db.relationship(
        'Product',
        backref='category',
        lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Category {self.name}>'
