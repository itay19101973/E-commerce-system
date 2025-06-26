from models.category import Category
from sqlalchemy import select
from database import get_db_connection
from models.product import Product

db = get_db_connection()


def get_category_name_by_id(category_id):
    get_category_name_stmt = select(Category.name).where(Category.id == category_id)
    result = db.session.execute(get_category_name_stmt).one_or_none()
    if result:
        return result[0]

    raise ValueError(f"category with id {category_id} doesn't exist.")


def get_category_id_by_name(category_name):
    get_category_id_stmt = select(Category.id).where(Category.name == category_name)
    result = db.session.execute(get_category_id_stmt).one_or_none()
    if result:
        return result[0]

    raise ValueError(f"category with id {category_name} doesn't exist.")


def get_all_categories():
    categories = Category.query.all()
    if not categories:
        raise Exception("failed to fetch the categories from db.")

    return categories


def get_products_by_category(category_name):
    category_id = get_category_id_by_name(category_name)

    get_products_by_category_stmt = select(Product.name).where(Product.category_id == category_id)
    result = db.session.execute(get_products_by_category_stmt).all()

    if result:
        return result

    raise ValueError(f"error occurred while fetching products from db")


def update_category_name(current_category_name, new_category_name):
    category = Category.query.filter_by(name=current_category_name).first()
    if not category:
        raise ValueError("invalid category name given, category to change wasn't found.")

    category.name = new_category_name
    db.session.commit()


def delete_category(category_to_delete):
    category = Category.query.filter_by(name=category_to_delete).first()
    if not category:
        raise ValueError("category wasn't found")

    db.session.delete(category)
    db.session.commit()
