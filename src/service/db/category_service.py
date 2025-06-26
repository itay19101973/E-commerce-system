from typing import List

from models.category import Category
from sqlalchemy import select
from database import get_db_connection
from models.product import Product

db = get_db_connection()


def get_category_name_by_id(category_id: int) -> str:
    """
       Retrieves the name of a category by its ID.

       Args:
           category_id: The ID of the category.

       Returns:
           The name of the category.

       Raises:
           ValueError: If no category with the given ID exists.
    """
    get_category_name_stmt = select(Category.name).where(Category.id == category_id)
    result = db.session.execute(get_category_name_stmt).one_or_none()
    if result:
        return result[0]

    raise ValueError(f"category with id {category_id} doesn't exist.")


def get_category_id_by_name(category_name: str) -> int:
    """
    Retrieves the ID of a category by its name.

    Args:
        category_name: The name of the category.

    Returns:
        The ID of the category.

    Raises:
        ValueError: If no category with the given name exists.
    """
    get_category_id_stmt = select(Category.id).where(Category.name == category_name)
    result = db.session.execute(get_category_id_stmt).one_or_none()
    if result:
        return result[0]

    raise ValueError(f"category with id {category_name} doesn't exist.")


def get_all_categories() -> List[Category]:
    """
    Retrieves all categories from the database.

    Returns:
        A list of Category objects.

    Raises:
        Exception: if category is None.
    """
    categories = Category.query.all()
    if categories is None:
        raise Exception("couldn't get the categories.")

    return categories


def get_products_by_category(category_name: str) -> List[str]:
    """
    Retrieves all product names belonging to a given category.

    Args:
        category_name: The name of the category.

    Returns:
        A list  containing product names.

    Raises:
        ValueError: If an error occurs while fetching products.
    """
    category_id = get_category_id_by_name(category_name)

    get_products_by_category_stmt = select(Product.name).where(Product.category_id == category_id)
    result = db.session.execute(get_products_by_category_stmt).all()

    if result:
        names = [row[0] for row in result]
        return names

    raise ValueError(f"error occurred while fetching products from db")


def update_category_name(current_category_name: str, new_category_name: str) -> None:
    """
    Updates the name of a category.

    Args:
        current_category_name: The current name of the category.
        new_category_name: The new name to assign.

    Raises:
        ValueError: If the category is not found.
    """
    category = Category.query.filter_by(name=current_category_name).first()
    if not category:
        raise ValueError("invalid category name given, category to change wasn't found.")

    category.name = new_category_name
    db.session.commit()


def delete_category(category_to_delete: str) -> None:
    """
    Deletes a category from the database.

    Args:
        category_to_delete: The name of the category to delete.

    Raises:
        ValueError: If the category is not found.
    """
    category = Category.query.filter_by(name=category_to_delete).first()
    if not category:
        raise ValueError("category wasn't found")

    db.session.delete(category)
    db.session.commit()
