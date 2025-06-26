from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class ProductInfo(BaseModel):
    id: int
    name: str
    quantity: int
    category: str
    price: int

    class Config:
        from_attributes = True
        orm_mode = True


class UpdateProduct(BaseModel):
    id: int
    name: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    price: Optional[int] = None
