from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class ProductInfo(BaseModel):
    """
    Schema representing full product information.

    Attributes:
        id: Unique identifier of the product.
        name: Name of the product.
        quantity: Number of items in stock.
        category: The category this product belongs to.
        price: Price of the product in integer units (e.g., cents or dollars).
    """
    id: int
    name: str
    quantity: int
    category: str
    price: int

    class Config:
        from_attributes = True
        orm_mode = True


class UpdateProduct(BaseModel):
    """
    Schema for updating product information.

    Attributes:
        id: The ID of the product to update.
        name: Optional new name of the product.
        quantity: Optional new stock quantity.
        category: Optional new category.
        price: Optional new price.
    """
    id: int
    name: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    price: Optional[int] = None
