from pydantic import BaseModel, EmailStr, constr


class ProductName(BaseModel):
    name: str


class ProductInfo(BaseModel):
    name: str
    quantity: int

    class Config:
        from_attributes = True
        orm_mode = True
