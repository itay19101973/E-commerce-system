# schemas/statistics.py
from pydantic import BaseModel
from typing import List


class ProductSalesPercentage(BaseModel):
    """
    Represents the overall sales statistics for a single product across all categories.

    Attributes:
        product_id (int): Unique identifier for the product.
        product_name (str): Name of the product.
        total_quantity_sold (int): Total quantity of the product sold.
        sales_percentage (float): Percentage of this product's sales out of all products sold.
    """
    product_id: int
    product_name: str
    total_quantity_sold: int
    sales_percentage: float

    class Config:
        from_attributes = True


class ProductSalesInCategory(BaseModel):
    """
    Represents the sales data of a single product within a specific category.

    Attributes:
        product_id (int): Unique identifier for the product.
        product_name (str): Name of the product.
        quantity_sold (int): Total quantity sold in this category.
        sales_percentage_within_category (float):
            Percentage of this product's sales relative to the total in the category.
    """
    product_id: int
    product_name: str
    quantity_sold: int
    sales_percentage_within_category: float

    class Config:
        from_attributes = True


class CategoryProductSales(BaseModel):
    """
    Represents aggregated sales statistics for a specific category,
    including a breakdown of each product's performance within the category.

    Attributes:
        category_id (int): Unique identifier for the category.
        category_name (str): Name of the category.
        total_category_quantity (int): Total quantity sold in the category.
        products (List[ProductSalesInCategory]):
            List of products and their sales statistics within the category.
    """
    category_id: int
    category_name: str
    total_category_quantity: int
    products: List[ProductSalesInCategory]

    class Config:
        from_attributes = True
