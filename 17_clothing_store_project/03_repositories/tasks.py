"""
Этап 03. Репозитории

Цель: вынести SQL-операции в отдельные классы-репозитории
и работать с уже подготовленной PostgreSQL-базой без ORM.

Репозитории создавайте прямо в этом файле.
Модели импортируйте из 01_domain_models/tasks.py.
"""


# Задание 1
# Импортируйте модели из файла 01_domain_models/tasks.py.
# Не копируйте классы моделей в файл репозиториев.
# Модели не должны знать, что данные хранятся в PostgreSQL.


# TODO: импортировать модели для работы репозиториев
import os
import psycopg2

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

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "clothing_store"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


# Задание 2
# Подключитесь к PostgreSQL через функцию из 02_postgresql_storage/tasks.py.
# Репозитории должны получать готовое соединение через __init__.


# TODO: подключить репозитории к готовому соединению

'''
Category =  (self, category_id, category_name, category_description):
Product =   (self, id, product_name, category_id, price, color, description, is_active):
LeftSizes = (self, store_id, product_id, size, quantity):
Byer =      (self, byer_id, byer_name, byer_email, byer_telephone):
'''

class SomeRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_categories(self, categories):
        query = """
            INSERT INTO categories (category_id, category_name, category_description)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (categories.category_id, categories.category_name, categories.category_description))

        self.connection.commit()

    def get_by_id_c(self, category_id):
        query = """
            SELECT category_id, category_name, category_description
            FROM books
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(row[0], row[1], row[2])
    

#-Product-------------------------------------------------------------------------------------------------------------------
    def add_product(self, product):
        query = """
            INSERT INTO product (product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active))

        self.connection.commit()

    def get_by_id_p(self, category_id):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM category_id
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
#-LeftSizes--------------------------------------------------------------------------------------------------------------------------------------
    def add_left_sizes(self, left_sizes):
        query = """
            INSERT INTO product (store_id, product_id, size, quantity)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (left_sizes.store_id, left_sizes.product_id, left_sizes.size, left_sizes.quantity))

        self.connection.commit()

    def get_by_id_ls(self, category_id):
        query = """
            SELECT store_id, product_id, size, quantity
            FROM store_id
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return LeftSizes(row[0], row[1], row[2], row[3])
    
#-Byer-------------------------------------------------------------------------------------------------------------------
    def add_byer(self, byer):
        query = """
            INSERT INTO product (byer_id, byer_name, byer_email, byer_telephone)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (byer.byer_id, byer.byer_name, byer.byer_email, byer.byer_telephone))

        self.connection.commit()

    def get_by_id_b(self, byer_id):
        query = """
            SELECT byer_id, byer_name, byer_email, byer_telephone
            FROM byer_id
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (byer_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Byer(row[0], row[1], row[2], row[3])
 

# Задание 3
# Создайте репозиторий категорий.
# Он должен добавлять категорию, находить ее по идентификатору и возвращать список категорий.


# TODO: добавить PostgreSQL-репозиторий категорий


# Задание 4
# Создайте репозиторий товаров.
# Он должен добавлять товар в таблицу и находить товар по идентификатору.


# TODO: добавить PostgreSQL-репозиторий товаров


# Задание 5
# Добавьте операции получения всех товаров, обновления и удаления.
# Продумайте поведение при повторном идентификаторе и при удалении
# несуществующего товара.


# TODO: расширить операции репозитория товаров


# Задание 6
# Создайте репозиторий остатков по размерам.
# Он должен позволять узнать, сколько единиц конкретного размера есть на складе.


# TODO: добавить PostgreSQL-репозиторий остатков по размерам


# Задание 7
# Создайте репозиторий покупателей.
# Его поведение должно быть похоже на репозиторий товаров.


# TODO: добавить PostgreSQL-репозиторий покупателей


# Задание 8
# Создайте несколько категорий, товаров, остатков и покупателей, сохраните их в PostgreSQL
# и проверьте основные операции через повторное чтение из базы.


# TODO: добавить ручную проверку репозиториев с реальной БД
category = Category(1,"Юбки","Женская одежда")
product = Product(1, "Короткая юбка",1 , 1000, "серая", "Юбка выше колен", "Продан")
left_sizes = LeftSizes(1, 1, "XL", 5)
byer = Byer (1, "Ivan", "Ivan@rambler.ru", "+79154908888")

print(category)
print(product)
print(left_sizes)
print(byer)
