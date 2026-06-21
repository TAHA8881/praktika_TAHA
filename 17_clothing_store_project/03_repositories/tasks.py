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

class CategoryRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_categories(self, categories):
        query = """
            INSERT INTO categories (id, name, description)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (categories.category_id, categories.category_name, categories.category_description))

        self.connection.commit()

    def get_by_id_c(self, category_id):
        query = """
            SELECT id, name, description
            FROM categories
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(row[0], row[1], row[2])
    
    def get_by_c_name(self, category_name):
        query = """
            SELECT id, name, description
            FROM categories
            WHERE name = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_name,))
            row = cursor.fetchone()
            if row:
                return Category(row[0], row[1], row[2])    
            return None
        
    def get_all(self):
        query = "SELECT id, name, description FROM categories ORDER BY id"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Category(row[0], row[1], row[2]) for row in rows]

    def update(self, category):
        query = """
            UPDATE categories SET name = %s, description = %s
            WHERE id = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (category.category_name, category.category_description, category.category_id))
            self.connection.commit()

    def delete(self, category_id):
        query = "DELETE FROM categories WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Категория с id {category_id} не найдена")
            self.connection.commit()

#-Product-------------------------------------------------------------------------------------------------------------------
class ProductRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_product(self, product):
        query = """
            INSERT INTO products (id, category_id, name, price, color, description, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product.id, product.category_id, product.product_name, product.price, product.color, product.description, product.is_active))

        self.connection.commit()

    def get_by_id_p(self, product_id):
        query = """
            SELECT id, category_id, name, price, color, description, is_active
            FROM products
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

        if row:

            return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
        return None
    
    def get_all(self, only_active=False):
        query = "SELECT id, category_id, name, price, color, description, is_active FROM products"
        params = []
        if only_active:
            query += " WHERE is_active = TRUE"
        query += " ORDER BY id"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def search_by_name(self, keyword, only_active=False):
        query = """
            SELECT id, category_id, name, price, color, description, is_active
            FROM products
            WHERE LOWER(name) LIKE LOWER(%s)
        """
        params = [f'%{keyword}%']
        if only_active:
            query += " AND is_active = TRUE"
        query += " ORDER BY name"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def filter_by_category(self, category_id, only_active=False):
        query = """
            SELECT id, category_id, name, price, color, description, is_active
            FROM products
            WHERE category_id = %s
        """
        params = [category_id]
        if only_active:
            query += " AND is_active = TRUE"
        query += " ORDER BY name"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def filter_by_color(self, color, only_active=False):
        query = """
            SELECT id, category_id, name, price, color, description, is_active
            FROM products
            WHERE LOWER(color) = LOWER(%s)
        """
        params = [color]
        if only_active:
            query += " AND is_active = TRUE"
        query += " ORDER BY name"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def filter_by_price_range(self, min_price, max_price, only_active=False):
        query = """
            SELECT id, category_id, name, price, color, description, is_active
            FROM products
            WHERE price BETWEEN %s AND %s
        """
        params = [min_price, max_price]
        if only_active:
            query += " AND is_active = TRUE"
        query += " ORDER BY price"
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def update(self, product):
        query = """
            UPDATE products SET
                category_id = %s,
                name = %s,
                price = %s,
                color = %s,
                description = %s,
                is_active = %s
            WHERE id = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (
                product.category_id,
                product.product_name,
                product.price,
                product.color,
                product.description,
                product.is_active,
                product.id
            ))
            if cursor.rowcount == 0:
                raise ValueError(f"Товар с id {product.id} не найден")
            self.connection.commit()


    def delete(self, product_id):
        query = "DELETE FROM products WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Товар с id {product_id} не найден")
            self.connection.commit()
    
#-LeftSizes--------------------------------------------------------------------------------------------------------------------------------------
class SizesRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_left_sizes(self, left_sizes):
        query = """
            INSERT INTO leftsizes (id, product_id, size, quantity)
            VALUES (%s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (left_sizes.store_id, left_sizes.product_id, left_sizes.size, left_sizes.quantity))

        self.connection.commit()

    def get_by_id_ls(self, leftsize_id):
        query = """
            SELECT store_id, product_id, size, quantity
            FROM leftsizes
            WHERE product_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (leftsize_id,))
            row = cursor.fetchone()

        if row:
            return LeftSizes(row[0], row[1], row[2], row[3])
        return None

    def get_by_product_and_size(self, product_id, size):
        query = "SELECT id, product_id, size, quantity FROM leftsizes WHERE product_id = %s AND size = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id, size))
            row = cursor.fetchone()
            if row:
                return LeftSizes(row[0], row[1], row[2], row[3])
            return None

    def get_by_product(self, product_id):
        query = "SELECT id, product_id, size, quantity FROM leftsizes WHERE product_id = %s ORDER BY size"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            rows = cursor.fetchall()
            return [LeftSizes(row[0], row[1], row[2], row[3]) for row in rows]

    def update_quantity(self, product_id, size, new_quantity):
        query = "UPDATE leftsizes SET quantity = %s WHERE product_id = %s AND size = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (new_quantity, product_id, size))
            if cursor.rowcount == 0:
                raise ValueError(f"Остаток для товара {product_id} размера {size} не найден")
            self.connection.commit()

    def decrease_quantity(self, product_id, size, amount):
        query = "UPDATE leftsizes SET quantity = quantity - %s WHERE product_id = %s AND size = %s AND quantity >= %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (amount, product_id, size, amount))
            if cursor.rowcount == 0:
                raise ValueError(f"Недостаточно остатка или запись не найдена для товара {product_id} размера {size}")
            self.connection.commit()

    def delete(self, leftsize_id):
        query = "DELETE FROM leftsizes WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (leftsize_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Запись остатка с id {leftsize_id} не найдена")
            self.connection.commit()


#-Byer-------------------------------------------------------------------------------------------------------------------
class ByerRepository:

    def __init__(self, connection):
        self.connection= connection 
    
    def add_byer(self, byer):
        query = """
            INSERT INTO customers (id, name, email, phone)
            VALUES (%s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (byer.byer_id, byer.byer_name, byer.byer_email, byer.byer_telephone))

        self.connection.commit()


    def get_all(self):
        query = """
            SELECT id, name, email, phone
            FROM customers
            ORDER BY id
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Byer(row[0], row[1], row[2], row[3]) for row in rows]

    def get_by_id_b(self, customer_id):
        query = """
            SELECT id, name, email, phone
            FROM customers
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
        if row:
            return Byer(row[0], row[1], row[2], row[3])
        return None
    
    def get_by_email(self, email):
        query = "SELECT id, name, email, phone FROM customers WHERE email = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                return Byer(row[0], row[1], row[2], row[3])
            return None

    def update(self, customer):
        query = """
            UPDATE customers SET name = %s, email = %s, phone = %s
            WHERE id = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (customer.byer_name, customer.byer_email, customer.byer_telephone, customer.byer_id))
            if cursor.rowcount == 0:
                raise ValueError(f"Покупатель с id {customer.byer_id} не найден")
            self.connection.commit()

    def delete(self, customer_id):
        query = "DELETE FROM customers WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Покупатель с id {customer_id} не найден")
            self.connection.commit()


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
#category = Category(1,"Юбки","Женская одежда")
#product = Product(1, "Короткая юбка",1 , 1000, "серая", "Юбка выше колен", False)
#left_sizes = LeftSizes(1, 1, "XL", 5)
#byer = Byer (1, "Ivan", "Ivan@rambler.ru", "+79154908888")

#print(category)
#print(product)
#print(left_sizes)
#print(byer)

if __name__ == "__main__":
    conn = get_connection()

    # Пример теста – создаём и читаем категорию, товар, остаток, покупателя
    cat_repo = CategoryRepository(conn)
    cat = Category(1, "Обувь", "Женская и мужская обувь")   # id=1 задаём явно
    cat_repo.add_categories(cat)
    print(cat_repo.get_by_id_c(1))

    prod_repo = ProductRepository(conn)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивная обувь", True)  # id=1
    prod_repo.add_product(prod)
    print(prod_repo.get_by_id_p(1))

    left_repo = SizesRepository(conn)
    left = LeftSizes(1, 1, "42", 10)  # store_id=1
    left_repo.add_left_sizes(left)
    print(left_repo.get_by_product_and_size(1, "42"))

    cust_repo = ByerRepository(conn)
    cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
    cust_repo.add_byer(cust)
    print(cust_repo.get_by_id_b(1))

    conn.close()