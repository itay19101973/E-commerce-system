import http

from flask import jsonify

from database import get_db_connection
from models.category import Category
from schemas.product import ProductInfo
from schemas.user import UserInfo

from models.product import Product


def get_product_by_name(product_name):
    product = Product.query.filter_by(name=product_name).first()

    if not product:
        raise ValueError(f"product with name {product_name} wasn't found.")

    return product


def add_products_to_db(df):
    """
    Adds or updates products in the database from a cleaned DataFrame.

    For each row in the DataFrame:
    - If a product with the same name already exists in the database, its quantity is updated (increased).
    - If the product does not exist, a new product record is created and added.

    :param df: pandas.DataFrame containing product data.
               Expected columns: 'name' (str), 'quantity' (int).
    :return: None
    """
    db = get_db_connection()

    # Add products to database
    for _, row in df.iterrows():
        # Check if product already exists
        existing_product = Product.query.filter_by(name=row['name']).first()

        if existing_product:
            continue
        else:
            category = Category.query.filter_by(name=row['category']).first()
            # Create new product
            new_product = Product(
                name=row['name'],
                quantity=row['quantity'],
                category_id=category.id
            )
            db.session.add(new_product)

    db.session.commit()
