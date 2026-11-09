import sqlite3
import os

DB_PATH = 'shop.db'


if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

db = sqlite3.connect(DB_PATH)
c = db.cursor()


with open('schema.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

c.executescript(sql)
db.commit()
print("База создана по схеме schema.sql")


print("\nПользователи в системе:")
c.execute("SELECT user_id, login, last_name, first_name, patronymic FROM users")
for row in c.fetchall():
    print(row)

db.close()
