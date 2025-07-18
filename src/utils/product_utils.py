from typing import List

import pandas as pd


def validate_product_csv(df: pd.DataFrame) -> List[str]:
    """
    checks if the product csv has the required colons and if so returns them
    :param df: the data frame
    :return: the required columns that needs to be in the product csv file
    """
    required_columns = ['name', 'quantity', 'category', 'price']
    if not all(col in df.columns for col in required_columns):
        print(f"CSV must contain columns: {required_columns}")
        print(f"Found columns: {list(df.columns)}")
        return []
    return required_columns


def clean_product_data(df: pd.DataFrame, required_columns: List[str]) -> pd.DataFrame:
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
    df['category'] = df['category'].astype(str)
    df['price'] = df['price'].astype(float)
    return df
