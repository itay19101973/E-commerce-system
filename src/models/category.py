from datetime import datetime
from database import get_db_connection

db = get_db_connection()


class Category(db.Model):
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
