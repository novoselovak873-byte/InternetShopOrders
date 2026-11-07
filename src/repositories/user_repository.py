from database.database import get_connection
from models.user import User

def create(login, password, role_id, fio=None, contact=None, address=None) -> int:
    # Добавление нового пользователя
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (login, password, role_id, fio, contact, address)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (login, password, role_id, fio, contact, address))
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_by_login(login) -> User | None:
    # Получение пользователя по его логину
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, login, password, role_id, fio, contact, address FROM users WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return User(*row) if row else None

def get_all_clients() -> list[User]:
    # Получение списка всех клиентов магазина
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, login, password, role_id, fio, contact, address FROM users WHERE role_id = 2")
    rows = cur.fetchall()
    conn.close()
    return [User(*r) for r in rows]
