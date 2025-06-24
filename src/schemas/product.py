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


