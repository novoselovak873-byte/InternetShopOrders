from database.database import get_connection
from models.product import Product

def get_by_id(product_id) -> Product | None:
    # Поиск товара по его ID
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, name, category, price, stock FROM products WHERE product_id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return Product(*row) if row else None

def get_all() -> list[Product]:
    # Получение списка всех товаров на складе
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, name, category, price, stock FROM products")
    rows = cur.fetchall()
    conn.close()
    return [Product(*r) for r in rows]

def update_stock(product_id, new_stock):
    # Обновление остатка товара на складе
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE products SET stock = ? WHERE product_id = ?", (new_stock, product_id))
    conn.commit()
    conn.close()
