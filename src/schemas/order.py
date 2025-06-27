from pydantic import BaseModel


class AddOrderItem(BaseModel):
    """
    Schema representing a single item in an order.

    Attributes:
        product_id: The unique identifier of the product to order.
        quantity: The number of units of the product being ordered.
    """
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    """
    Schema for creating a new order.

    Attributes:
        items: A list of products and their quantities to be included in the order.
    """
    items: list[AddOrderItem]


class ExecuteOrder(BaseModel):
    id: int
