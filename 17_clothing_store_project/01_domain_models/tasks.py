"""
Этап 01. Доменные модели магазина одежды

Цель: описать основные объекты предметной области без подключения к БД,
меню, репозиториев и сервисов.

Модели создавайте прямо в этом файле. Следующие этапы будут импортировать
их отсюда, а не копировать классы заново.
"""


# Задание 1
# Опишите модель категории одежды.
# Категория должна хранить идентификатор, название и краткое описание.


# TODO: добавить модель категории

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



# Задание 2
# Опишите модель товара.
# Продумайте поля для идентификатора, названия, категории, цены, цвета,
# описания и активности товара.


# TODO: добавить модель товара

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
        if  is_active == "":
            raise ValueError("Активность товара не может быть пустым")
        
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



# Задание 3
# Добавьте проверки для данных товара.
# Обратите внимание на цену, пустое название и связь с категорией.



# TODO: добавить защиту состояния товара
"см задание выше"


# Задание 4
# Опишите модель остатка товара по размеру.
# Она должна связывать товар, размер и количество этого размера на складе.


# TODO: добавить модель остатка по размеру

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
       


# Задание 5
# Добавьте поведение товара.
# Товар или отдельная модель остатка должны помогать понять,
# доступен ли конкретный размер и какое количество можно купить.


# TODO: добавить методы изменения и проверки товара



# Задание 6
# Опишите модель покупателя.
# Продумайте поля для идентификатора, имени, телефона и email.


# TODO: добавить модель покупателя
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
    
# Задание 7
# Создайте несколько объектов и проверьте, что корректные данные принимаются,
# а некорректные приводят к понятной ошибке.

'''(self, category_id, category_name, category_description):
(self, id, product_name, category_id, price, color, description, is_active):
(self, store_id, product_id, size, quantity):
(self, byer_id, byer_name, byer_email, byer_telephone):
'''
# TODO: добавить ручную проверку моделей

category = Category(1,"Юбки","Женская одежда")
product = Product(1, "Короткая юбка",1 , 1000, "серая", "Юбка выше колен", "Продан")
left_sizes = LeftSizes(1, 1, "XL", 5)
byer = Byer (1, "Ivan", "Ivan@rambler.ru", "+79154908888")

print(category)
print(product)
print(left_sizes)
print(byer)