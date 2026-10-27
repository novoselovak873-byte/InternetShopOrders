DROP TABLE IF EXISTS order_list;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS managers;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fio TEXT NOT NULL,
    phone TEXT,
    email TEXT
);

CREATE TABLE managers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fio TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    manager_id INTEGER,
    order_date TEXT,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES clients (id),
    FOREIGN KEY (manager_id) REFERENCES managers (id)
);

CREATE TABLE order_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

INSERT INTO clients (fio, phone, email) VALUES 
('Иванов И.И.', '+79991112233', 'ivanov@mail.ru'),
('Петрова А.С.', '89994445566', 'petrova_anna@yandex.ru');

INSERT INTO managers (fio, phone) VALUES 
('Сидоров П.П.', '+79120001122');

INSERT INTO products (title, price, stock) VALUES 
('Ноутбук Lenovo', 55000, 10),
('Мышь беспроводная', 1500, 50),
('Клавиатура механическая', 4500, 20);

INSERT INTO orders (client_id, manager_id, order_date, status) VALUES 
(1, 1, '25.10.2023', 'Оплачен'),
(2, 1, '26.10.2023', 'В обработке');

INSERT INTO order_list (order_id, product_id, qty) VALUES 
(1, 1, 1),
(1, 2, 1),
(2, 3, 1);
