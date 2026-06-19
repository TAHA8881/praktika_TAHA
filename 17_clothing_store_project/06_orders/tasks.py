"""
Этап 06. Заказы

Цель: оформить заказ из корзины, зафиксировать позиции и уменьшить остатки
товаров на складе.

Модели заказа, репозиторий заказов и сервис заказов создавайте прямо в этом файле.
Корзину, товары, покупателей и репозитории импортируйте из предыдущих этапов.
"""

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

# Задание 1 :))))
# Импортируйте модели товара, остатка по размеру, покупателя, корзины и репозитории.
# Для проверки нужны товары с ограниченным остатком конкретных размеров.


# TODO: подготовить основу для оформления заказа


# Задание 2
# Расширьте SQL-схему таблицами заказов и позиций заказов.
# Продумайте внешние ключи на покупателя, заказ и товар.


# TODO: добавить таблицы заказов в schema.sql


# Задание 3
# Опишите позицию заказа.
# Она должна хранить снимок покупки: идентификатор товара, название товара,
# выбранный размер, цену за единицу и количество.


# TODO: добавить модель позиции заказа
class OrderItems:
    def __init__id__(self, id, order_id, product_id, product_name, size, price, quantity):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.size = size
        self.price = price
        self.quantity = quantity

# Задание 4
# Опишите заказ.
# Продумайте идентификатор, покупателя, позиции, сумму и статус.


# TODO: добавить модель заказа
class Order:
    STATUSES = ["создан", "оплачен", 'передан в доставку', 'выполнен', 'отменен']

    def __init__(self, id, customer_id, total_price, status):

        self.id = id
        self.customer_id = customer_id
        self.total_price = total_price
        self.status = status
        

        if id < 0:
            raise ValueError("Идентификатор товара должен быть положительным")
        
        if status not in self.STATUSES:
            raise ValueError("Таких статусов нет.  Напишите 1 из следующих статусов: создан, оплачен, передан в доставку, выполнен, отменен")
        
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
        query = """INSERT INTO order (id, user_id, total_price,status) VALUES (%s, %s, %s, %s)"""
        
        with self.connection.cursor() as cursor:
            cursor.execute(query, (order.id, order.customer_id, order.total_price, order.status))
            for item in order.items:
                query_items =  """INSERT INTO order_items (id, order_id, clothes_id, clothes_name, size, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query_items, (
                item.id,
                order.id,
                item.clothes_id,                
                item.clothes_name,
                item.size,
                item.price,
                item.quantity
            ))
        self.connection.commit()

    def get_order_history(self, user_id):
        query="""SELECT id, user_id, total_price, status, created_at
                FROM orders
                WHERE user_id s%
                ORDERBY created_at DESC"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            orders = cursor.fetchall()

            result = []
            for order_row in orders:
                order_dict = {
                    'id' : order_row[0],
                    'user_id' : order_row[1],
                    'total_price' : order_row[2],
                    'status' : order_row[3],
                    'created_at' : order_row[4],
                    'items' : self._get_order_items(order_row[0])
                }
                result.append(order_dict)
            return result
        
    def _get_order_items(self, order_id):
        query="""SELECT id, clothes_id, clothes_name, size, price, quantity
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
class ClothingService:
    def create_clothing(self, size, product):
        if not product.Product():
            raise ValueError("Покупка не возможна")
        if not size.LeftSizes():
            raise ValueError("Нет такого размера")


# Задание 7
# Добавьте списание остатков со склада после успешного оформления.
# Списание должно уменьшать остаток именно выбранного размера.
# Ошибка в середине оформления не должна оставлять данные в странном состоянии.

    
# TODO: добавить безопасное списание остатков
class Tranzactia:
#    def spisanie(self, a, OpisanieZakaza.total_price, CartProduct.price):
    def spisanie(self, a):
        if self.status == "выполнен":
            a = OpisanieZakaza.total_price - price.CartProduct
            return a

# Задание 8
# Оберните оформление заказа в транзакцию.
# Создание заказа, создание позиций и списание остатков должны быть одной операцией.


# TODO: добавить транзакционное оформление заказа



class Tranzactia:
    def vizov_func():
        CartProduct()
        Cart()
        PoziciaZakaza()
        ClothingService()

# Задание 9
# Проверьте успешное оформление и несколько ошибок: пустая корзина,
# нехватка товара, неизвестный покупатель.
# Проверьте, что при ошибке данные в БД не остаются частично измененными.


# TODO: добавить ручную проверку заказов
