from database.database import get_connection
from models.user import User

def create(login, password, role_id, last_name=None, first_name=None, patronymic=None, contact=None, address=None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (login, password, role_id, last_name, first_name, patronymic, contact, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (login, password, role_id, last_name, first_name, patronymic, contact, address))
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_by_login(login) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, login, password, role_id, last_name, first_name, patronymic, contact, address 
        FROM users WHERE login = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return User(*row) if row else None

def get_all_clients() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, login, password, role_id, last_name, first_name, patronymic, contact, address 
        FROM users WHERE role_id = 2
    """)
    rows = cur.fetchall()
    conn.close()
    return [User(*r) for r in rows]
