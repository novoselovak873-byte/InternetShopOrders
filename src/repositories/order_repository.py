from database.database import get_connection
from models.order import Order, OrderItem
from datetime import datetime

def create(user_id, total_amount, payment_method, status_id=1) -> int:
    conn = get_connection()
    cur = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO orders (user_id, order_date, total_amount, payment_method, status_id)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, now_str, total_amount, payment_method, status_id))
    order_id = cur.lastrowid
    conn.commit()
    conn.close()
    return order_id

def create_item(order_id, product_id, quantity, price_per_item):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, price_per_item)
        VALUES (?, ?, ?, ?)
    """, (order_id, product_id, quantity, price_per_item))
    conn.commit()
    conn.close()

def get_by_id(order_id) -> Order | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.order_id, o.user_id, o.order_date, o.total_amount, o.payment_method, o.status_id, o.delivery_date, s.name,
               (u.last_name || ' ' || u.first_name || ' ' || u.patronymic) as client_fio
        FROM orders o
        JOIN statuses s ON o.status_id = s.status_id
        JOIN users u ON o.user_id = u.user_id
        WHERE o.order_id = ?
    """, (order_id,))
    row = cur.fetchone()
    conn.close()
    return Order(*row) if row else None

def get_items(order_id) -> list[OrderItem]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT oi.item_id, oi.order_id, oi.product_id, oi.quantity, oi.price_per_item, p.name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return [OrderItem(*r) for r in rows]

def get_all() -> list[Order]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.order_id, o.user_id, o.order_date, o.total_amount, o.payment_method, o.status_id, o.delivery_date, s.name,
               (u.last_name || ' ' || u.first_name || ' ' || u.patronymic) as client_fio
        FROM orders o
        JOIN statuses s ON o.status_id = s.status_id
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [Order(*r) for r in rows]

def get_by_user_id(user_id) -> list[Order]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.order_id, o.user_id, o.order_date, o.total_amount, o.payment_method, o.status_id, o.delivery_date, s.name,
               (u.last_name || ' ' || u.first_name || ' ' || u.patronymic) as client_fio
        FROM orders o
        JOIN statuses s ON o.status_id = s.status_id
        JOIN users u ON o.user_id = u.user_id
        WHERE o.user_id = ?
        ORDER BY o.order_id DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [Order(*r) for r in rows]

def update_status(order_id, status_id, delivery_date=None):
    conn = get_connection()
    cur = conn.cursor()
    if delivery_date:
        cur.execute("UPDATE orders SET status_id = ?, delivery_date = ? WHERE order_id = ?", (status_id, delivery_date, order_id))
    else:
        cur.execute("UPDATE orders SET status_id = ? WHERE order_id = ?", (status_id, order_id))
    conn.commit()
    conn.close()
