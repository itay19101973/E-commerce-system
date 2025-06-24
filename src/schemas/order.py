from pydantic import BaseModel


class AddOrderItem(BaseModel):
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    user_id: int
    items: list[AddOrderItem]
