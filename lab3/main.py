import sqlite3

db = sqlite3.connect('shop.db')
c = db.cursor()

# читаем sql файл
f = open('schema.sql', 'r', encoding='utf-8')
sql = f.read()
f.close()

c.executescript(sql)
db.commit()
print("База создана")

# клиенты
print("Клиенты:")
c.execute("SELECT * FROM clients")
for row in c.fetchall():
    print(row)

# заказы
print("Заказы:")
c.execute("SELECT orders.id, clients.fio, orders.status FROM orders JOIN clients ON orders.client_id = clients.id")
for row in c.fetchall():
    print(row)

# состав 1 заказа
print("Состав 1 заказа:")
c.execute("SELECT products.title, order_list.qty FROM order_list JOIN products ON order_list.product_id = products.id WHERE order_list.order_id = 1")
for row in c.fetchall():
    print(row)

db.close()