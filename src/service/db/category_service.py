from models.category import Category
from sqlalchemy import select
from database import get_db_connection

db = get_db_connection()


def get_category_name_by_id(category_id):
    get_category_name_stmt = select(Category.name).where(Category.id == category_id)
    result = db.session.execute(get_category_name_stmt).one_or_none()
    if result:
        return result[0]

    raise ValueError(f"category with id {category_id} doesn't exist.")


