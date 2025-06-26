import pandas as pd

from database import get_db_connection
from models.category import Category

from models.product import Product
from schemas.product import UpdateProduct

db = get_db_connection()


def get_product_by_name(product_name: str) -> Product:
    """
    Retrieve a product by its name.

    Args:
        product_name: The name of the product to find.

    Raises:
        ValueError: If no product with the given name exists.

    Returns:
        Product: The found product instance.
    """
    product = Product.query.filter_by(name=product_name).first()

    if not product:
        raise ValueError(f"product with name {product_name} wasn't found.")

    return product


def parse_products_df_to_db(df: pd.DataFrame) -> None:
    """
    Add or update products in the database from a cleaned DataFrame.

    For each row:
    - Attempts to add the product. If a duplicate name is found, logs the error.

    Args:
        df: pandas DataFrame with columns: 'name', 'quantity', 'category', 'price'.

    Returns:
        None
    """
    # Add products to database
    for _, row in df.iterrows():
        try:
            add_product_to_db(row['name'], row['quantity'], row['category'], row['price'], commit=False)
        except ValueError as e:
            print(f"error while inserting product to db: {str(e)}")

    db.session.commit()


def add_product_to_db(name: str, quantity: int, category_name: str, price: int, commit: bool = True) -> Product:
    """
    Add a new product to the database.

    Args:
        name: Product name.
        quantity: Quantity of the product.
        category_name: Category name for the product.
        price: Price of the product.
        commit: Whether to commit the transaction immediately.

    Raises:
        ValueError: If product name already exists or category does not exist.

    Returns:
        Product: The newly created product instance.
    """
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


def remove_product(product_id: int, commit: bool = True) -> None:
    """
    Remove a product by its ID.

    Args:
        product_id: The ID of the product to remove.
        commit: Whether to commit the transaction immediately.

    Raises:
        ValueError: If the product with given ID does not exist.

    Returns:
        None
    """
    product = Product.query.get(product_id)
    if not product:
        raise ValueError(f"product with id :{product_id} doesnt exist.")

    db.session.delete(product)

    if commit:
        db.session.commit()


def update_product(new_product_details: UpdateProduct) -> Product:
    """
    Update an existing product's details.

    Args:
        new_product_details: An object with attributes id, name, price, quantity, category.

    Raises:
        ValueError: If the product to edit is not found or if price/quantity values are invalid.

    Returns:
        Product: The updated product instance.
    """
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



