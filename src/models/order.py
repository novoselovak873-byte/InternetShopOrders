from dataclasses import dataclass


@dataclass
class Order:
    # Модель заказа
    order_id: int
    user_id: int
    order_date: str
    total_amount: float
    payment_method: str
    status_id: int
    delivery_date: str | None = None

    # Служебные поля для вывода в консоль
    status_name: str | None = None
    client_fio: str | None = None


@dataclass
class OrderItem:
    # Модель позиции внутри заказа
    item_id: int
    order_id: int
    product_id: int
    quantity: int
    price_per_item: float
    product_name: str | None = None
