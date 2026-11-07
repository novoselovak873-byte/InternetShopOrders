import sys
import os

# Добавление папки src в пути поиска Python, чтобы не ломались импорты
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import init_db
from services import auth_service
from ui.menu import manager_menu, client_menu, warehouse_menu


def main():
    # Создание файлов базы данных при первом запуске
    init_db()

    while True:
        print("\n" + "=" * 45)
        print(" ИС УЧЕТА ЗАКАЗОВ В ИНТЕРНЕТ-МАГАЗИНЕ ")
        print("=" * 45)
        print("1. Вход в систему (Авторизация)")
        print("0. Завершить работу")

        choice = input("Выберите действие: ")
        if choice == "1":
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            user = auth_service.authenticate(login, password)

            if not user:
                print("Ошибка! Неверный логин или пароль.")
                continue

            print(f"\nУспешный вход в систему!")

            # Разграничение интерфейса по ролям пользователей
            if user.role_id == 1:
                manager_menu(user)
            elif user.role_id == 2:
                client_menu(user)
            elif user.role_id == 3:
                warehouse_menu(user)

        elif choice == "0":
            print("Программа закрыта.")
            break


if __name__ == "__main__":
    main()
