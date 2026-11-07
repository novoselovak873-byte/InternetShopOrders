from dataclasses import dataclass

@dataclass
class Product:
    # Модель товара на складе
    product_id: int
    name: str
    category: str
    price: float
    stock: int
