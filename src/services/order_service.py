from repositories import order_repository, product_repository
from models.order import Order
from datetime import datetime

def create_order(user_id, cart: dict[int, int], payment_method) -> int:
    if not cart:
        raise Exception("Корзина пуста!")
    total_amount = 0.0
    validated_items = []
    for p_id, qty in cart.items():
        if qty <= 0:
            continue
        product = product_repository.get_by_id(p_id)
        if not product:
            raise Exception(f"Товар с ID {p_id} не найден!")
        if product.stock < qty:
            raise Exception(f"Товара '{product.name}' недостаточно (в наличии: {product.stock})!")
        total_amount += product.price * qty
        validated_items.append((product, qty))
    order_id = order_repository.create(user_id, total_amount, payment_method, status_id=1)
    for product, qty in validated_items:
        order_repository.create_item(order_id, product.product_id, qty, product.price)
        product_repository.update_stock(product.product_id, product.stock - qty)
    return order_id

def pay_order(order_id):
    order = order_repository.get_by_id(order_id)
    if not order:
        raise Exception("Заказ не найден!")
    if order.status_id != 1:
        raise Exception("Оплатить можно только заказ в статусе 'В сборке'!")
    order_repository.update_status(order_id, status_id=2)

def cancel_order(order_id):
    order = order_repository.get_by_id(order_id)
    if not order:
        raise Exception("Заказ не найден!")
    # ИСПРАВЛЕНО: Изменили синтаксис на сравнение через логическое ИЛИ (or)
    # 3 - Выполнен, 4 - Отменен
    if order.status_id == 3 or order.status_id == 4:
        raise Exception("Нельзя отменить выполненный или уже отмененный заказ!")
    items = order_repository.get_items(order_id)
    for item in items:
        product = product_repository.get_by_id(item.product_id)
        if product:
            product_repository.update_stock(item.product_id, product.stock + item.quantity)
    order_repository.update_status(order_id, status_id=4)

def complete_order(order_id):
    order = order_repository.get_by_id(order_id)
    if not order:
        raise Exception("Заказ не найден!")
    if order.status_id != 2:
        raise Exception("Выдать можно только оплаченный заказ!")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_repository.update_status(order_id, status_id=3, delivery_date=now_str)

def get_financial_report():
    orders = order_repository.get_all()
    completed_orders = [o for o in orders if o.status_id == 3]
    total_profit = sum(o.total_amount for o in completed_orders)
    return {
        "total_orders_count": len(orders),
        "completed_count": len(completed_orders),
        "total_profit": total_profit
    }
