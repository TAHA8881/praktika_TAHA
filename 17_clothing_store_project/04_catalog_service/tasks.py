"""
Этап 04. Сервис каталога

Цель: вынести логику просмотра, поиска и фильтрации товаров в отдельный
сервисный слой.

Сервис каталога создавайте прямо в этом файле.
Репозитории импортируйте из 03_repositories/tasks.py.
"""


# Задание 1
# Импортируйте модели, репозитории товаров, категорий и остатков по размерам.
# Добавьте несколько товаров разных категорий, цветов, размеров, цен и остатков.

#--------------------------------------------------------------------------------------
# Опишите модель категории одежды.
# Категория должна хранить идентификатор, название и краткое описание.


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

# Импортируйте модели из файла 01_domain_models/tasks.py.
# Не копируйте классы моделей в файл репозиториев.
# Модели не должны знать, что данные хранятся в PostgreSQL.

# Подключитесь к PostgreSQL через функцию из 02_postgresql_storage/tasks.py.
# Репозитории должны получать готовое соединение через __init__.



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
            WHERE category_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(row[0], row[1], row[2])
    
    def get_by_c_name(self, category_name):
        query = """
            SELECT category_id, category_name, category_description
            FROM categories
            WHERE category_name = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_name,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(row[0], row[1], row[2])
   
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
            cursor.execute(query, (product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active))

        self.connection.commit()

    def get_by_id_p(self, product_id):
        query = """
            SELECT product.id, product.category_id, product.product_name, product.price, product.color, product.description, product.is_active
            FROM products
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get_by_active_status(self, is_active):

        if not isinstance(is_active, bool):
            raise ValueError("is_active должен быть булевым значением")
    
        query = """
            SELECT id, product_name, category_id, price, color, description, is_active
            FROM products
            WHERE is_active = %s
        """
    
        with self.connection.cursor() as cursor:
            cursor.execute(query, (is_active,))
            row = cursor.fetchall()  
    
        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get_by_p_n(self, product_name):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM products
            WHERE product_name = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_name,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get_by_id_p_a(self, is_active):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM products
            WHERE is_active = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (is_active,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get_by_c(self, color):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM products
            WHERE color = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (color,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get_by_p(self, min_price, max_price):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM products
            WHERE price BETWEEN %s AND %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (min_price, max_price,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
#-LeftSizes--------------------------------------------------------------------------------------------------------------------------------------
class SizesRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_left_sizes(self, left_sizes):
        query = """
            INSERT INTO left_sizes (id, product_id, size, quantity)
            VALUES (%s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (left_sizes.store_id, left_sizes.product_id, left_sizes.size, left_sizes.quantity))

        self.connection.commit()

    def get_by_id_ls(self, product_id):
        query = """
            SELECT store_id, product_id, size, quantity
            FROM left_sizes
            WHERE product_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return LeftSizes(row[0], row[1], row[2], row[3])
    
    def get_by_size(self, size):
        query = """
            SELECT store_id, product_id, size, quantity
            FROM left_sizes
            WHERE size = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (size,))
            row = cursor.fetchone()

        if row is None:
            return None

        return LeftSizes(row[0], row[1], row[2], row[3])
    
#-Byer-------------------------------------------------------------------------------------------------------------------
class ByerRepository:

    def __init__(self, connection):
        self.connection= connection 
    
    def add_byer(self, byer):
        query = """
            INSERT INTO byer (id, name, email, phone)
            VALUES (%s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (byer.byer_id, byer.byer_name, byer.byer_email, byer.byer_telephone))

        self.connection.commit()

    def get_all(self):
        query = """
            SELECT id, byer_name, byer_email, byer_telephone
            FROM byer
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        customers = []

        for row in rows:
            customer = Byer(row[0], row[1], row[2], row[3])
            customers.append(customer)

        return customers

    def get_by_id_b(self, byer_id):
        query = """
            SELECT byer_id, byer_name, byer_email, byer_telephone
            FROM byer
            WHERE byer_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (byer_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Byer(row[0], row[1], row[2], row[3])
 
#---------------------------------------------------------------------------------------------------------

category = Category(1,"Юбки","Женская одежда")
product = Product(1, "Короткая юбка",1 , 1000, "серая", "Юбка выше колен", False)
left_sizes = LeftSizes(1, 1, "XL", 5)
byer = Byer (1, "Ivan", "Ivan@rambler.ru", "+79154908888")

print(category)
print(product)
print(left_sizes)
print(byer)

# TODO: подготовить данные каталога


# Задание 2 ✔
# Создайте сервис каталога, который получает репозиторий товаров.
# При необходимости передайте в сервис репозиторий категорий и репозиторий остатков.
# Сервис должен работать через методы репозиториев, а не через внешний список.


# TODO: добавить сервис каталога


# Задание 3 ✔
# Добавьте получение активных товаров.
# Неактивные товары не должны попадать в обычную выдачу каталога.


# TODO: добавить выдачу активных товаров


# Задание 4 ✔
# Добавьте поиск по части названия.
# Поиск должен быть удобным для пользователя и не зависеть от регистра.


# TODO: добавить поиск по названию


# Задание 5 ✔ 
# Добавьте фильтрацию по категории ✔ , размеру ✔, цвету ✔ и диапазону цены ✔ .
# Фильтр по размеру должен учитывать наличие товара именно этого размера.
# Фильтры можно реализовать постепенно.


# TODO: добавить фильтрацию каталога


# Задание 6 ✔ 
# Добавьте сортировку найденных товаров.
# Продумайте варианты сортировки по цене и названию.


# TODO: добавить сортировку каталога


# Задание 7
# Проверьте сервис на нескольких сценариях поиска и фильтрации.


# TODO: добавить ручную проверку сервиса каталога
