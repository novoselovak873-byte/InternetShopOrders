from dataclasses import dataclass

@dataclass
class Order:
    order_id: int
    user_id: int
    order_date: str
    total_amount: float
    payment_method: str
    status_id: int
    delivery_date: str | None = None
    status_name: str | None = None
    client_fio: str | None = None

@dataclass
class OrderItem:
    item_id: int
    order_id: int
    product_id: int
    quantity: int
    price_per_item: float
    product_name: str | None = None
