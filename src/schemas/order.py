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
        location: a string with country name
        items: A list of products and their quantities to be included in the order.
    """
    location: str
    items: list[AddOrderItem]


class ExecuteOrder(BaseModel):
    """
    Represents a request to execute an order.

    Attributes:
        id (int): The ID of the order to be executed.
    """
    id: int


class UpdateOrderInput(BaseModel):
    """
    Schema for updating an existing order.

    Attributes:
        id (int): The unique identifier of the order to update.
        items (List[AddOrderItem]): A list of new items to replace the current order items.
    """
    id: int
    items: list[AddOrderItem]
    location: str = None


class OrderItemInfo(BaseModel):
    """
    Schema representing a single item in an order response.

    Attributes:
        name (str): The name of the product.
        quantity (int): The quantity of the product in the order.
    """
    name: str
    quantity: int

    class Config:
        from_attributes = True
        orm_mode = True


class OrderInfo(BaseModel):
    """
    Schema representing full order details for responses.

    Attributes:
        id (int): The unique ID of the order.
        items (List[OrderItemInfo]): A list of items in the order with product names and quantities.
    """
    id: int
    items: list[OrderItemInfo]
    location: str

    class Config:
        from_attributes = True
        orm_mode = True


class DeleteOrderInput(BaseModel):
    """
    Schema for deleting an order.

    Attributes:
        id (int): The ID of the order to delete.
    """
    id: int


class SalesInfo(BaseModel):
    """
    Data model representing sales summary information.

    Attributes:
        number_of_executed_orders (int): The total number of orders marked as executed.
        total_profit (float): The total profit calculated from all executed orders.
    """
    number_of_executed_orders: int
    total_profit: float

    class Config:
        from_attributes = True
