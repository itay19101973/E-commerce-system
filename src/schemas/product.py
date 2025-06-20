from pydantic import BaseModel, EmailStr, constr


class ProductInfo(BaseModel):
    name: str
    quantity: int
    category: str

    class Config:
        from_attributes = True
        orm_mode = True
