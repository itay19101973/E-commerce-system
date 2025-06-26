from datetime import datetime
from database import get_db_connection

db = get_db_connection()


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): Primary key.
        email (str): User's unique email.
        password_hash (str): Hashed password.
        full_name (str): User's full name.
        orders (List[Order]): List of orders associated with the user.
        created_at (datetime): Timestamp when user was created.
        updated_at (datetime): Timestamp when user was last updated.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    orders = db.relationship('Order', backref='user', lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'
