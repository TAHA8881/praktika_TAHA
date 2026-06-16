"""
Этап 05. Корзина

Цель: реализовать добавление товаров в корзину, изменение количества,
удаление позиций и подсчет итоговой суммы.

Модели и сервис корзины создавайте прямо в этом файле.
Товар, остатки и сервис каталога импортируйте из предыдущих этапов.
"""


# Задание 1:)
# Импортируйте модели товара, остатков по размерам и сервис каталога.
# Для проверки создайте несколько товаров с разными остатками по размерам.
#---______-________-_________-_---------_____________-------------____________________________________________________________________________________________________________________________________________________________________________________________________________________

#--------------------------------------------------------------------------------------
# Опишите модель категории одежды.
# Категория должна хранить идентификатор, название и краткое описание.



class Category:
    def __init__(self, category_id, category_name, category_description):
        if category_id == "":
            raise ValueError("Идентификатор товара не может быть пустым")
        if category_name == "":
            raise ValueError("Продукт не может быть пустым")
        if  category_description == "":
            raise ValueError("Описание товара не может быть пустым")

        self.category_id = category_id
        self.category_name = category_name
        self.category_description = category_description

    def __str__(self):
        return(f'{self.category_id}, {self.category_name}, {self.category_description}')
    def __repr__(self):
        return(f'{self.category_id}, {self.category_name}, {self.category_description}')




# Опишите модель товара.
# Продумайте поля для идентификатора, названия, категории, цены, цвета,
# описания и активности товара.


class Product:
    def __init__(self, id, product_name, category_id, price, color, description, is_active):
        if id < 0:
            raise ValueError("Идентификатор товара должен быть положительным")
        if product_name == "":
            raise ValueError("Название товара не может быть пустым")
        if category_id < 0:
            raise ValueError("Категория товара не может отрицательной")
        if price <0:
            raise ValueError("Не может быть, чтобы цена продуктов была меньше 0")
        if  color == "":
            raise ValueError("Цвет товара не может быть пустым")
        if  description == "":
            raise ValueError("Описание товара не может быть пустым")
        if not isinstance(is_active, bool):
            raise ValueError("Активность товара должна быть булевым значением (True/False)")
        
        self.id = id
        self.product_name = product_name
        self.category_id = category_id
        self.price = price
        self.color = color
        self.description = description
        self.is_active = is_active

    def __str__(self):
        return(f'{self.id}, {self.product_name}, {self.category_id}, {self.price}, {self.color}, {self.description}, {self.is_active}')
    def __repr__(self):
        return(f'{self.id}, {self.product_name}, {self.category_id}, {self.price}, {self.color}, {self.description}, {self.is_active}')


class LeftSizes:
    SIZES= ["XS", "S", 'L', 'M', 'XL', 'XXL']

    def __init__(self, store_id, product_id, size, quantity):
        

        if size not in self.SIZES:
            raise ValueError("Таких размеров одежды нет")
        
        self.store_id = store_id
        self.product_id = product_id
        self.size = size
        self.quantity = quantity

    def is_available(self):
        return self.quantity > 0

    def __str__(self):
        return(f'{self.store_id}, {self.product_id}, {self.size}, {self.quantity}')
    def __repr__(self):
        return(f'{self.store_id}, {self.product_id}, {self.size}, {self.quantity}')
       



# Добавьте поведение товара.
# Товар или отдельная модель остатка должны помогать понять,
# доступен ли конкретный размер и какое количество можно купить.


# добавить методы изменения и проверки товара




# Опишите модель покупателя.
# Продумайте поля для идентификатора, имени, телефона и email.


# добавить модель покупателя
class Byer:

    def __init__(self, byer_id, byer_name, byer_email, byer_telephone):
        if byer_id <= 0:
            raise ValueError("Идентификатор покупателя  должен быть положительным")

        if byer_name == "":
            raise ValueError("Имя покупателя не может быть пустым")

        if "@" not in byer_email:
            raise ValueError("Некорректный email")

        if  byer_telephone == "":
            raise ValueError("Телефон покупателя не может быть пустым")

        self.byer_id = byer_id
        self.byer_name = byer_name
        self.byer_email = byer_email
        self.byer_telephone = byer_telephone

    def __str__(self):
        return(f'{self.byer_id}, {self.byer_name}, {self.byer_email}, {self.byer_telephone}')
    def __repr__(self):
        return(f'{self.byer_id}, {self.byer_name}, {self.byer_email}, {self.byer_telephone}')
#----------------------------------------------------------------------------------------------
# Импортируйте модели из файла 01_domain_models/tasks.py.
# Не копируйте классы моделей в файл репозиториев.
# Модели не должны знать, что данные хранятся в PostgreSQL.

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



# Подключитесь к PostgreSQL через функцию из 02_postgresql_storage/tasks.py.
# Репозитории должны получать готовое соединение через __init__.




#import os
#import psycopg2

#from importlib import import_module
#from pathlib import Path
#import sys

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
            INSERT INTO categoriy (category_id, category_name, category_description)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (categories.category_id, categories.category_name, categories.category_description))

        self.connection.commit()

    def get_by_id_c(self, category_id):
        query = """
            SELECT category_id, category_name, category_description
            FROM category
            WHERE category_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(row[0], row[1], row[2])
    
    def get_by_id_c_id(self, category_name):
        query = """
            SELECT category_id, category_name, category_description
            FROM category
            WHERE category_name = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (category_name,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Category(row[0], row[1], row[2])
    
#-Product-------------------------------------------------------------------------------------------------------------------
    def add_product(self, product):
        query = """
            INSERT INTO product (product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active))

        self.connection.commit()

    def get_by_id_p(self, id):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM product
            WHERE id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get__by_active_status(self, is_active):

        if not isinstance(is_active, bool):
            raise ValueError("is_active должен быть булевым значением")
    
        query = """
            SELECT id, product_name, category_id, price, color, description, is_active
            FROM product
            WHERE is_active = %s
        """
    
        with self.connection.cursor() as cursor:
            cursor.execute(query, (is_active,))
            row = cursor.fetchall()  
    
        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6] )
    
    def get_by_p_n(self, product_name):
        query = """
            SELECT product.id, product.product_name, product.category_id, product.price, product.color, product.description, product.is_active
            FROM product
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
            FROM product
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
            FROM product
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
            FROM product
            WHERE price BETWEEN %s AND %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (min_price, max_price,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
#-LeftSizes--------------------------------------------------------------------------------------------------------------------------------------
    def add_left_sizes(self, left_sizes):
        query = """
            INSERT INTO product (store_id, product_id, size, quantity)
            VALUES (%s, %s, %s)
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (left_sizes.store_id, left_sizes.product_id, left_sizes.size, left_sizes.quantity))

        self.connection.commit()

    def get_by_id_ls(self, store_id):
        query = """
            SELECT store_id, product_id, size, quantity
            FROM left_sizes
            WHERE store_id = %s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (store_id,))
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

#---_______-____________________-_________________-___________-_____________________________------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO: подготовить товары для корзины


# Задание 2
# Опишите позицию корзины.
# В позиции должны быть товар, выбранный размер, количество и цена товара.


# TODO: добавить модель позиции корзины
class Cart:
    def __init__(self):
        self._items = []

    def add_cart_product(self, product):
        self._items.append(product)

    def total_price(self):
        total = 0

        for product in self._items:
            total += product.price

        return total

    def clear(self):
        self._items.clear()

# Задание 3
# Опишите корзину.
# Она должна хранить набор позиций одного покупателя.
# На этом этапе корзина может жить в памяти текущего запуска программы.


# TODO: добавить модель корзины


# Задание 4
# Добавьте добавление товара в корзину.
# Учтите размер, количество и доступный остаток именно выбранного размера.


# TODO: добавить добавление позиции


# Задание 5
# Добавьте изменение количества и удаление позиции.
# Продумайте поведение при нулевом количестве.


# TODO: добавить изменение и удаление позиции


# Задание 6
# Добавьте расчет итоговой суммы и очистку корзины.


# TODO: добавить сумму и очистку корзины


# Задание 7
# При необходимости создайте сервис корзины.
# Он может проверять доступность товара через сервис каталога или репозиторий остатков.


# TODO: отделить бизнес-проверки корзины от пользовательского ввода


# Задание 8
# Проверьте сценарий: добавить товар, увеличить количество, удалить позицию,
# снова добавить товар и посчитать итог.


# TODO: добавить ручную проверку корзины
