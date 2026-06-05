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

class SomeRepository:
    def __init__(self, connection):
        self.connection = connection

    def add(self, book):
        query = """
            INSERT INTO books (id, title, author)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (book.book_id, book.title, book.author))

        self.connection.commit()

    def get_by_id(self, book_id):
        query = """
            SELECT id, title, author
            FROM books
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (book_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Book(row[0], row[1], row[2])
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
