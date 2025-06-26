import pandas as pd

from utils.category_utils import add_categories_to_db
from utils.general import validate_file_path
from utils.product_utils import validate_product_csv, clean_product_data
from service.db.product_service import parse_products_df_to_db


def load_products_from_csv(csv_file_path: str) -> None:
    """
    Loads and validates product data from a CSV file, then inserts it into the database.

    Expected CSV columns:
    - name (str)
    - quantity (int)
    - price (int/float)
    - category (str)

    Process:
    1. Validates the CSV file path.
    2. Reads the CSV into a pandas DataFrame.
    3. Validates required columns exist.
    4. Cleans and converts the data.
    5. Adds any new categories.
    6. Adds the product entries.

    :param csv_file_path: Path to the CSV file containing product data.
    :raises RuntimeError: If file path or CSV structure is invalid.
    :return: None
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

