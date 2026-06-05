"""
Тема 10. Классы-модели
"""


# Задание 1
# Создайте модель User.
# Атрибуты: name, email, age.
# Добавьте метод get_info(), который возвращает строку с данными пользователя.


# TODO: решение
print(" ")
print("№1")
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return {
            "name": self.name,
            "email": self.email,
            "age" : self.age,
        }
    
user = User("Ivan", "Ivan@gmail.com", 20) 

user.get_info()
print(user.get_info())

'''
rectangle = Rectangle(10, 5)
rectangle.area()
rectangle.perimeter()

print(rectangle.area)
print(rectangle.perimeter)
'''

# Задание 2
# Добавьте в User валидацию возраста.
# Если age меньше 0, выбрасывайте ValueError.


# TODO: решение
print(" ")
print("№2")
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return {
            "name": self.name,
            "email": self.email,
            "age" : self.age,
        }
    
user = User("Ivan", "Ivan@gmail.com", -1) 

user.get_info()
print(user.get_info())
if user.age<0:
    print ('ValueError')


# Задание 3
# Создайте модель Product.
# Атрибуты: title, price, count.
# Добавьте метод get_total_price(), который возвращает price * count.
# Добавьте проверку: price и count не могут быть отрицательными.


# TODO: решение
# print(" ")
# print("№3")
# class Product:
#     def __init__(self, title, price,count):
#         if price < 0:
#             raise ValueError("Цена не может быть отрицательной")
#         if count < 0:
#             raise ValueError("Количество не может быть отрицательным")

#         self.title = title
#         self.price = price
#         self.count= count

#     def get_total_price(self):
#         print(self.price * self.count)
#         return self.price * self.count
    
# product = Product(10, 5, 6)
# product.get_total_price()
# print(product.get_total_price)




# Задание 4
# Создайте модель Task.
# Атрибуты: title, is_done.
# При создании is_done должен быть False.
# Добавьте методы mark_done() и mark_undone().


# TODO: решение
print(" ")
print("№4")
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True

    def mark_undone(self):
        self._undone = False

# Задание 5
# Добавьте в Task метод to_dict().
# Он должен возвращать словарь:
# {"title": ..., "is_done": ...}


# TODO: решение
print(" ")
print("№5")
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True

    def mark_undone(self):
        self._undone = False
    
    def to_dict(self):
        return {
            "title": self.title,
            "is_done": self.is_done,
        }
    
# task = Task("Ivan@gmail.com", False) 
# task.mark_done()
# task.mark_undone()
# task.to_dict()
# print(task.to_dict())

'''
print(" ")
print("№2")
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return {
            "name": self.name,
            "email": self.email,
            "age" : self.age,
        }
    
user = User("Ivan", "Ivan@gmail.com", -1) 

user.get_info()
print(user.get_info())
if user.age<0:
    print ('ValueError')
'''


# Задание 6
# Создайте модель Order.
# Атрибуты: customer_name, products.
# products — список объектов Product.
# Добавьте метод get_total(), который возвращает сумму всех товаров.


# TODO: решение
print(" ")
print("№6")
class Order:
    def __init__(self, customer_name, products):
        self.customer_name = customer_name
        self.products = products

    def get_total(self):
        sum = 0
        for product in self.products:
            sum += product.get_total_price()

        return sum
       
class Product:
    def __init__(self, title, price,count):
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if count < 0:
            raise ValueError("Количество не может быть отрицательным")

        self.title = title
        self.price = price
        self.count= count

    def get_total_price(self):
        return self.price * self.count
    
product1 = Product("Молоко", 5, 6)
product2 = Product("Чай", 10, 6)
product3 = Product("Кофе", 50, 6)
products = [product1, product2, product3]
order = Order("Ivan", products) 
print(order.get_total())
