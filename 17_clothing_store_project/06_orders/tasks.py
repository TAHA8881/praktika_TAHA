"""
Этап 06. Заказы

Цель: оформить заказ из корзины, зафиксировать позиции и уменьшить остатки
товаров на складе.

Модели заказа, репозиторий заказов и сервис заказов создавайте прямо в этом файле.
Корзину, товары, покупателей и репозитории импортируйте из предыдущих этапов.
"""

# Задание 1 :))))
# Импортируйте модели товара, остатка по размеру, покупателя, корзины и репозитории.
# Для проверки нужны товары с ограниченным остатком конкретных размеров.


# TODO: подготовить основу для оформления заказа

from importlib import import_module
from pathlib import Path
import sys

PROJECT_ROOT = Path (__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain_models.Product
Category = domain_models.Category
LeftSizes = domain_models.LeftSizes
Byer = domain_models.Byer

repos = import_module("17_clothing_store_project.03_repositories.tasks")
ProductRepository = repos.ProductRepository
SizesRepository = repos.SizesRepository
ByerRepository = repos.ByerRepository
get_connection = repos.get_connection

cart_module = import_module("17_clothing_store_project.05_cart.tasks")
CartService = cart_module.CartService
Cart = cart_module.Cart

# Задание 2
# Расширьте SQL-схему таблицами заказов и позиций заказов.
# Продумайте внешние ключи на покупателя, заказ и товар.


# TODO: добавить таблицы заказов в schema.sql


# Задание 3
# Опишите позицию заказа.
# Она должна хранить снимок покупки: идентификатор товара, название товара,
# выбранный размер, цену за единицу и количество.


# TODO: добавить модель позиции заказа
class OrderItem:
    def __init__(self, id, order_id, product_id, product_name, size, price, quantity):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.size = size
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

# Задание 4
# Опишите заказ.
# Продумайте идентификатор, покупателя, позиции, сумму и статус.


# TODO: добавить модель заказа
class Order:
    STATUSES = ["создан", "оплачен", 'передан в доставку', 'выполнен', 'отменен']

    def __init__(self, id=None, customer_id=None, items=None, status="создан", promocode=None):
        self.id = id  
        self.customer_id = customer_id
        self.items = items if items else []
        self.status = status
        self.promocode = promocode
        
        # сумма до скидки
        self.total_original = sum(item.total() for item in self.items)
        self.discount = 0
        self.total_final = self.total_original

        if id is not None and id < 0:
            raise ValueError("Идентификатор товара должен быть положительным")
        
        if status not in self.STATUSES:
            raise ValueError("Таких статусов нет.  Напишите 1 из следующих статусов: создан, оплачен, передан в доставку, выполнен, отменен")

    def apply_discount(self, discount_amount):
        if discount_amount > self.total_original:
            raise ValueError("Скидка не может превышать сумму заказа")
        self.discount = discount_amount
        self.total_final = self.total_original - discount_amount

    def cancel(self):
        if self.status == "выполнен":
            raise ValueError("Нельзя отменить завершенную запись")

        self.status = "отменен"

# Задание 5 есть
# Создайте репозиторий заказов.
# Он должен сохранять заказ и позиции заказа в PostgreSQL,
# а также позволять получить историю заказов покупателя.


# TODO: добавить репозиторий заказов

class OrderRepository:
    def __init__(self,connection):
        self.connection = connection

    def add_order(self, order):
        query = """INSERT INTO orders (customer_id, total_original, discount, total_final, status, promocode_used) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"""
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, (                order.customer_id,
                order.total_original,
                order.discount,
                order.total_final,
                order.status,
                order.promocode))
            
            order_id = cursor.fetchone()[0]
            order.id = order_id

            for item in order.items:
                item.order_id = order_id
                cursor.execute( """
                    INSERT INTO order_items (order_id, product_id, product_name, size, price, quantity)
                    VALUES (%s, %s, %s, %s, %s, %s)""", (
                    item.id,
                    order.id,
                    item.clothes_id,                
                    item.clothes_name,
                    item.size,
                    item.price,
                    item.quantity
                ))
        self.connection.commit()
        return order

    def get_order_history(self, customer_id):
        query="""
            SELECT id, customer_id, total_original, discount, total_final, status, created_at
            FROM orders
            WHERE user_id %s
            ORDER BY created_at DESC
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            rows = cursor.fetchall()
            result = []
            for row in rows:
                order_dict = {
                    'id' : row[0],
                    'user_id' : row[1],
                    'total_price' : row[2],
                    'status' : row[3],
                    'created_at' : row[4],
                    'items' : self._get_order_items(row[0])
                }
                result.append(order_dict)
            return result
        
    def _get_order_items(self, order_id):
        query="""
            SELECT id, product_id, product_name, size, price, quantity
            FROM order_items
                WHERE order_id = s%"""
            
        with self.connection.cursor() as cursor:
            cursor.execute(query, (order_id,))
            items = cursor.fetchall()

            return  [
                {
                    'id' : item[0],
                    'clothes_id' : item[1],
                    'clothes_name' : item[2],
                    'size' : item[3],
                    'price' : item[4],
                    'quantity' : item[5]
                }
                for item in items
            ]
        
    def get_order_by_id(self, order_id):
        query="""SELECT id, user_id, total_price, status, created_at
                FROM orders
                WHERE id s%"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (order_id,))
            order = cursor.fetchall()

        if order_id:
                return {
                    'id' : order[0],
                    'user_id' : order[1],
                    'total_price' : order[2],
                    'status' : order[3],
                    'created_at' : order[4],
                    'items' : self._get_order_items(order[0])
                }
        return None


# Задание 6
# Создайте сервис заказов.
# Он должен оформлять заказ из корзины и проверять, что покупка возможна
# для каждого выбранного размера.


# TODO: добавить сервис оформления заказа


class OrderService:
    def __init__(self, order_repo, product_repo, sizes_repo, customer_repo):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.sizes_repo = sizes_repo
        self.customer_repo = customer_repo

    # ← создание заказа из корзины
    def create_order(self, cart_service, customer_id, promocode=None):
        # ← проверяем, что покупатель существует
        customer = self.customer_repo.get_by_id_b(customer_id)
        if customer is None:
            raise ValueError(f"Покупатель с id {customer_id} не найден")

        # ← проверяем, что корзина не пуста
        if cart_service.cart.is_empty():
            raise ValueError("Корзина пуста")

        # ← формируем позиции заказа, проверяем остатки
        order_items = []
        for cart_item in cart_service.get_cart_items():
            # проверяем остаток
            leftover = self.sizes_repo.get_by_product_and_size(cart_item.product_id, cart_item.size)
            if leftover is None or leftover.quantity < cart_item.quantity:
                available = leftover.quantity if leftover else 0
                raise ValueError(f"Недостаточно товара id={cart_item.product_id}, размер {cart_item.size}. Доступно: {available}")
            # получаем название товара для снимка
            product = self.product_repo.get_by_id_p(cart_item.product_id)
            if product is None:
                raise ValueError(f"Товар с id {cart_item.product_id} не найден")
            order_item = OrderItem(
                id=None,
                order_id=None,
                product_id=cart_item.product_id,
                product_name=product.product_name,
                size=cart_item.size,
                price=cart_item.price,
                quantity=cart_item.quantity
            )
            order_items.append(order_item)

        # ← создаём объект заказа
        order = Order(customer_id=customer_id, items=order_items, promocode=promocode)

        # ← если есть промокод, применяем скидку (пока просто заглушка, потом подключим сервис скидок)
        if promocode:
            # здесь будет вызов DiscountService, но пока оставим
            pass

        # ← транзакционное сохранение заказа и списание остатков
        with self.order_repo.connection as conn:
            with conn.cursor() as cursor:
                try:
                    # 1. Сохраняем заказ (внутри вставляются и позиции)
                    self.order_repo.add_order(order)

                    # 2. Списываем остатки
                    for item in order_items:
                        self.sizes_repo.decrease_quantity(item.product_id, item.size, item.quantity)

                    # 3. Очищаем корзину
                    cart_service.clear_cart()

                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    raise e

        return order  


# Задание 7
# Добавьте списание остатков со склада после успешного оформления.
# Списание должно уменьшать остаток именно выбранного размера.
# Ошибка в середине оформления не должна оставлять данные в странном состоянии.

    
# TODO: добавить безопасное списание остатков


# Задание 8
# Оберните оформление заказа в транзакцию.
# Создание заказа, создание позиций и списание остатков должны быть одной операцией.


# TODO: добавить транзакционное оформление заказа


# Задание 9
# Проверьте успешное оформление и несколько ошибок: пустая корзина,
# нехватка товара, неизвестный покупатель.
# Проверьте, что при ошибке данные в БД не остаются частично измененными.


# TODO: добавить ручную проверку заказов

if __name__ == "__main__":
    conn = get_connection()

    # Создаём репозитории
    product_repo = ProductRepository(conn)
    sizes_repo = SizesRepository(conn)
    customer_repo = ByerRepository(conn)
    order_repo = OrderRepository(conn)

    # Подготавливаем данные
    try:
        # покупатель
        cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
        customer_repo.add_byer(cust)
    except Exception:
        pass

    try:
        # товар
        prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
        product_repo.add_product(prod)
    except Exception:
        pass

    try:
        # остаток
        left = LeftSizes(1, 1, "42", 10)
        sizes_repo.add_left_sizes(left)
    except Exception:
        pass

    # Создаём сервис корзины и добавляем товар
    cart_service = CartService(product_repo, sizes_repo)
    try:
        cart_service.add_to_cart(1, "42", 3)
        print("В корзину добавлено 3 шт. товара 1 размера 42")
    except Exception as e:
        print("Ошибка добавления в корзину:", e)

    # Сервис заказов
    order_service = OrderService(order_repo, product_repo, sizes_repo, customer_repo)

    # Успешное оформление заказа
    try:
        order = order_service.create_order(cart_service, 1)
        print(f"Заказ оформлен, id={order.id}, сумма={order.total_final}")
    except Exception as e:
        print("Ошибка оформления заказа:", e)

    # Проверка истории заказов
    history = order_repo.get_order_history(1)
    print("История заказов покупателя 1:", history)

    # Ошибочный сценарий: нехватка товара
    try:
        cart_service.add_to_cart(1, "42", 20)  # остаток был 10, уже списано 3, осталось 7
        order_service.create_order(cart_service, 1)
    except Exception as e:
        print("Ожидаемая ошибка (нехватка):", e)

    conn.close()