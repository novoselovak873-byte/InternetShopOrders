from repositories import product_repository, user_repository, order_repository
from services import auth_service, order_service
from models.user import User


def client_menu(user: User):
    # Текстовое меню для роли Клиент
    cart = {}
    while True:
        print(f"\n=== МЕНЮ КЛИЕНТА: {user.fio or user.login} ===")
        print("1. Посмотреть каталог товаров")
        print("2. Добавить товар в корзину")
        print("3. Посмотреть корзину и оформить заказ")
        print("4. Мои заказы (Отследить статус)")
        print("5. Оплатить заказ")
        print("6. Отменить заказ")
        print("0. Выход из аккаунта")

        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                products = product_repository.get_all()
                print("\nКаталог товаров магазина:")
                for p in products:
                    print(f"ID: {p.product_id} | {p.name} [{p.category}] - {p.price} руб. (Остаток: {p.stock})")
            elif choice == "2":
                p_id = int(input("Введите ID товара: "))
                qty = int(input("Введите количество: "))
                product = product_repository.get_by_id(p_id)
                if not product:
                    print("Товар не найден!")
                    continue
                cart[p_id] = cart.get(p_id, 0) + qty
                print(f"Товар '{product.name}' добавлен в корзину.")
            elif choice == "3":
                if not cart:
                    print("Ваша корзина пуста!")
                    continue
                print("\nСодержимое корзины:")
                total = 0
                for p_id, qty in cart.items():
                    p = product_repository.get_by_id(p_id)
                    print(f"- {p.name} x {qty} шт. = {p.price * qty} руб.")
                    total += p.price * qty
                print(f"Итого к оплате: {total} руб.")

                confirm = input("Оформить заказ? (да/нет): ").lower()
                if confirm in ["да", "yes", "y"]:
                    pm = input("Способ оплаты (Онлайн / При получении): ")
                    order_id = order_service.create_order(user.user_id, cart, pm)
                    print(f"Заказ №{order_id} успешно оформлен! Статус: В сборке.")
                    cart = {}
            elif choice == "4":
                orders = order_repository.get_by_user_id(user.user_id)
                if not orders:
                    print("История заказов пуста.")
                for o in orders:
                    print(
                        f"Заказ №{o.order_id} от {o.order_date} | Сумма: {o.total_amount} руб. | Статус: {o.status_name} | Оплата: {o.payment_method}")
            elif choice == "5":
                order_id = int(input("Введите номер заказа для оплаты: "))
                order_service.pay_order(order_id)
                print("Оплата подтверждена! Статус заказа: 'Оплачен'.")
            elif choice == "6":
                order_id = int(input("Введите номер заказа для отмены: "))
                order_service.cancel_order(order_id)
                print("Заказ отменен. Товар возвращен на склад.")
            elif choice == "0":
                break
        except Exception as e:
            print(f"Ошибка: {e}")


def manager_menu(user: User):
    # Текстовое меню для роли Менеджер (это ты)
    while True:
        print(f"\n=== МЕНЮ МЕНЕДЖЕРА: {user.fio or user.login} ===")
        print("1. Ручная регистрация нового клиента")
        print("2. Просмотр зарегистрированных клиентов")
        print("3. Просмотр всех заказов магазина")
        print("4. Фиксация прибыли (Финансовый отчет)")
        print("0. Выход из аккаунта")

        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                login = input("Логин клиента: ")
                password = input("Пароль: ")
                fio = input("ФИО клиента: ")
                contact = input("Телефон: ")
                address = input("Адрес доставки: ")
                c_id = auth_service.register_client(login, password, fio, contact, address)
                print(f"Клиент добавлен в БД с ID: {c_id}")
            elif choice == "2":
                clients = user_repository.get_all_clients()
                print("\nСписок клиентов в системе:")
                for c in clients:
                    print(f"ID: {c.user_id} | Логин: {c.login} | ФИО: {c.fio} | Тел: {c.contact}")
            elif choice == "3":
                orders = order_repository.get_all()
                print("\nВсе заказы в интернет-магазине:")
                for o in orders:
                    print(
                        f"Заказ №{o.order_id} | Клиент: {o.client_fio} | Статус: {o.status_name} | Сумма: {o.total_amount} руб.")
            elif choice == "4":
                rep = order_service.get_financial_report()
                print("\n===== ФИНАНСОВЫЙ ОТЧЕТ ИНТЕРНЕТ-МАГАЗИНА =====")
                print(f"Всего заказов в БД: {rep['total_orders_count']}")
                print(f"Из них успешно выполнены: {rep['completed_count']}")
                print(f"Общая зафиксированная чистая прибыль: {rep['total_profit']} руб.")
                print("==============================================")
            elif choice == "0":
                break
        except Exception as e:
            print(f"Ошибка: {e}")


def warehouse_menu(user: User):
    # Текстовое меню для роли Склад
    while True:
        print(f"\n=== ИНТЕРФЕЙС СКЛАДА: {user.fio or user.login} ===")
        print("1. Проверить остатки товаров на складе")
        print("2. Просмотреть электронные листы сборки")
        print("3. Выдать собранный и упакованный заказ")
        print("0. Выход из аккаунта")

        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                products = product_repository.get_all()
                print("\nАктуальные остатки склада:")
                for p in products:
                    print(f"ID: {p.product_id} | {p.name} | В наличии: {p.stock} шт.")
            elif choice == "2":
                orders = order_repository.get_all()
                print("\nЭлектронные листы сборки:")
                for o in orders:
                    print(f"Лист сборки для Заказа №{o.order_id} | Текущий статус: {o.status_name}")
            elif choice == "3":
                order_id = int(input("Введите номер оплаченного заказа для выдачи: "))
                order_service.complete_order(order_id)
                print(f"Заказ №{order_id} успешно выдан клиенту! Статус изменен на 'Выполнен'.")
            elif choice == "0":
                break
        except Exception as e:
            print(f"Ошибка склада: {e}")
