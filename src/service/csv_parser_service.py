import pandas as pd

from utils.category_utils import add_categories_to_db
from utils.general import validate_file_path
from models.product import Product
from utils.product_utils import validate_product_csv, clean_product_data
from service.db.product_service import parse_products_df_to_db


def load_products_from_csv(csv_file_path):
    """
    Load products from CSV file and add them to the database.
    Expected CSV columns: name, quantity
    """
    if not validate_file_path(csv_file_path):
        raise RuntimeError("invalid csv file path")

    # Read CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Clean column names (remove whitespace)
    df.columns = df.columns.str.strip()

    # Validate csv ( check that the csv got the colons we need)
    required_columns = validate_product_csv(df)
    if not required_columns:
        raise RuntimeError("csv product file doesnt contain the required columns")

    # Clean data
    df = clean_product_data(df, required_columns)

    # add products and categories to the database
    add_categories_to_db(df)
    parse_products_df_to_db(df)

