

from database import get_db_connection
from models.category import Category

from models.product import Product

db = get_db_connection()


def get_product_by_name(product_name):
    product = Product.query.filter_by(name=product_name).first()

    if not product:
        raise ValueError(f"product with name {product_name} wasn't found.")

    return product


def parse_products_df_to_db(df):
    """
    Adds or updates products in the database from a cleaned DataFrame.

    For each row in the DataFrame:
    - If a product with the same name already exists in the database, its quantity is updated (increased).
    - If the product does not exist, a new product record is created and added.

    :param df: pandas.DataFrame containing product data.
               Expected columns: 'name' (str), 'quantity' (int).
    :return: None
    """

    # Add products to database
    for _, row in df.iterrows():
        try:
            add_product_to_db(row['name'], row['quantity'], row['category'], row['price'], commit=False)
        except ValueError as e:
            print(f"error while inserting product to db: {str(e)}")

    db.session.commit()


def add_product_to_db(name, quantity, category_name, price, commit=True):
    existing_product = Product.query.filter_by(name=name).first()

    if existing_product:
        raise ValueError(f"product with name {name} already exists.")

    category = Category.query.filter_by(name=category_name).first()

    if not category:
        raise ValueError(f"category with name {category_name} doesn't exist.")

    # Create new product
    new_product = Product(
        name=name,
        quantity=quantity,
        category_id=category.id,
        price=price
    )
    db.session.add(new_product)

    if commit:
        db.session.commit()

    return new_product


def remove_product(product_id, commit=True):
    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"product with id :{product_id} doesnt exist.")

    db.session.delete(product)

    if commit:
        db.session.commit()


def update_product(new_product_details):
    product = Product.query.filter_by(id=new_product_details.id).first()
    if not product:
        raise ValueError("product to edit wasn't found.")

    if new_product_details.name:
        product.name = new_product_details.name

    if new_product_details.price:
        if new_product_details.price > 0:
            product.price = new_product_details.price
        else:
            raise ValueError("product price must be > 0")

    if new_product_details.quantity:
        if new_product_details.quantity >= 0:
            product.quantity = new_product_details.quantity
        else:
            raise ValueError("product quantity must be >= 0")

    if new_product_details.category:
        category = Category.query.filter_by(name=new_product_details.category).first()
        if not category:
            category = Category(name=new_product_details.category)
            db.session.add(category)
            db.session.flush()
        product.category_id = category.id

    db.session.commit()
    return product



