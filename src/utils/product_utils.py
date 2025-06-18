from db import get_db_connection
import pandas as pd
from utils.general import validate_file_path
from models.product import Product


def load_products_from_csv(csv_file_path):
    """
    Load products from CSV file and add them to the database.
    Expected CSV columns: name, quantity
    """
    if not validate_file_path(csv_file_path):
        raise RuntimeError("invalid csv file path")

    try:
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

        # add products to the database
        add_products_to_db(df)

    except Exception as e:
        print(f"error caught in function 'load product from csv' {str(e)}")


def validate_product_csv(df):
    """
    checks if the product csv has the required colons and if so returns them
    :param df: the data frame
    :return: the required columns that needs to be in the product csv file
    """
    required_columns = ['name', 'quantity']
    if not all(col in df.columns for col in required_columns):
        print(f"CSV must contain columns: {required_columns}")
        print(f"Found columns: {list(df.columns)}")
        return []
    return required_columns


def clean_product_data(df, required_columns):
    """
    Cleans and validates a DataFrame containing product data.

    :param df: pandas.DataFrame containing the product data to clean.
    :param required_columns: List of column names that must not contain null values.
    :return: Cleaned pandas.DataFrame with valid product data.
    """
    df = df.dropna(subset=required_columns)  # Remove rows with missing required data
    df['name'] = df['name'].str.strip()  # Remove whitespace from names
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')  # Convert to numeric
    df = df.dropna(subset=['quantity'])  # Remove rows with invalid quantities
    df['quantity'] = df['quantity'].astype(int)  # Convert to integer
    return df


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
            # Update existing product
            existing_product.quantity += row['quantity']
        else:
            # Create new product
            new_product = Product(
                name=row['name'],
                quantity=row['quantity']
            )
            db.session.add(new_product)

    db.session.commit()

