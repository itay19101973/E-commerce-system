from pydantic import BaseModel, EmailStr, constr


class CategoryInfo(BaseModel):
    name: str
    products: list[str]

    class Config:
        from_attributes = True
        orm_mode = True