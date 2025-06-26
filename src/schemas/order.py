from pydantic import BaseModel


class AddOrderItem(BaseModel):
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    items: list[AddOrderItem]
