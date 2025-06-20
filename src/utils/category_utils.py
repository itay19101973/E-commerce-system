from database import get_db_connection
from models.category import Category


def add_categories_to_db(df):
    """
    Adds or updates categories in the database from a cleaned DataFrame.

    For each row in the DataFrame:
    - If a category with the same name already exists in the database, its quantity is updated (increased).
    - If the category does not exist, a new category record is created and added.

    :param df: pandas.DataFrame containing category data.
               Expected columns: 'name' (str), 'quantity' (int).
    :return: None
    """
    db = get_db_connection()

    # Add categories to database
    for _, row in df.iterrows():
        # Check if category already exists
        existing_category = Category.query.filter_by(name=row['category']).first()

        if existing_category:
            continue
        else:

            # Create new category
            new_category = Category(
                name=row['category']
            )
            db.session.add(new_category)

    db.session.commit()