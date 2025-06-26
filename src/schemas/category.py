from pydantic import BaseModel, EmailStr, constr


class CategoryInfo(BaseModel):
    """
    Schema representing a product category and its associated products.

    Attributes:
        name: The name of the category.
        products: A list of product names that belong to this category.
    """
    name: str
    products: list[str]

    class Config:
        from_attributes = True
        orm_mode = True

