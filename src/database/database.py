import sqlite3

DB_NAME = "shop.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Таблица ролей пользователей
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Таблица статусов заказов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS statuses (
            status_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Таблица пользователей (менеджеры, клиенты, склад)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            fio TEXT,
            contact TEXT,
            address TEXT,
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        )
    """)

    # Таблица товаров на складе
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Таблица заказов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status_id INTEGER NOT NULL,
            delivery_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (status_id) REFERENCES statuses(status_id)
        )
    """)

    # Таблица позиций заказа (содержимое корзины)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_item REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Заполнение справочников
    cur.execute("INSERT OR IGNORE INTO roles VALUES (1, 'Менеджер')")
    cur.execute("INSERT OR IGNORE INTO roles VALUES (2, 'Клиент')")
    cur.execute("INSERT OR IGNORE INTO roles VALUES (3, 'Склад')")

    cur.execute("INSERT OR IGNORE INTO statuses VALUES (1, 'В сборке')")
    cur.execute("INSERT OR IGNORE INTO statuses VALUES (2, 'Оплачен')")
    cur.execute("INSERT OR IGNORE INTO statuses VALUES (3, 'Выполнен')")
    cur.execute("INSERT OR IGNORE INTO statuses VALUES (4, 'Отменен')")

    # Тестовые учетные записи персонала
    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, login, password, role_id, fio) VALUES (1, 'manager', '123', 1, 'Новоселова Карина Сергеевна')")
    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, login, password, role_id, fio) VALUES (2, 'sklad', '123', 3, 'Сотрудник Склада Петров')")

    # Тестовые товары
    cur.execute(
        "INSERT OR IGNORE INTO products (product_id, name, category, price, stock) VALUES (1, 'Смартфон X', 'Электроника', 50000.0, 10)")
    cur.execute(
        "INSERT OR IGNORE INTO products (product_id, name, category, price, stock) VALUES (2, 'Ноутбук Y', 'Электроника', 90000.0, 5)")
    cur.execute(
        "INSERT OR IGNORE INTO products (product_id, name, category, price, stock) VALUES (3, 'Наушники Z', 'Аксессуары', 5000.0, 25)")

    conn.commit()
    conn.close()
