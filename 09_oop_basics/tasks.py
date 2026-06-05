"""
Тема 9. Основы ООП: классы и объекты
"""


# Задание 1
# Создайте класс Student.
# В __init__ сохраните name и age.
# Создайте объект и выведите его имя и возраст.


# TODO: решение
print(" ")
print("№1")
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Anna", 18)

print(student.name)
print(student.age)

# Задание 2
# Добавьте в класс Student метод greet().
# Метод должен возвращать строку:
# Привет, меня зовут <name>.


# TODO: решение
print(" ")
print("№2")
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def greet(self):
        print(f"Привет, меня зовут {self.name}")

student = Student("Anna", 18)
student.greet()

print(student.name)
print(student.age)

# Задание 3
# Создайте класс Product с атрибутами title и price.
# Добавьте метод get_info(), который возвращает строку:
# <title>: <price> руб.


# TODO: решение
print(" ")
print("№3")
class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def get_info(self):
        print(self.title,":", self.price, " руб.")

product = Product("Book", 500)
product.get_info()

print(product.title)
print(product.price)



# Задание 4
# Создайте класс Rectangle с атрибутами width и height.
# Добавьте метод area(), который возвращает площадь.
# Добавьте метод perimeter(), который возвращает периметр.


# TODO: решение
print(" ")
print("№4")
class Rectangle:
    def __init__(self, width, height):
        self.width=width
        self.height=height

    def area(self):
        print(1/2*self.width*self.height, "- Площадь")

    def perimeter(self):
        print(2*1/2*self.width*self.height/self.height, "- Периметр")

rectangle = Rectangle(10, 5)
rectangle.area()
rectangle.perimeter()

print(rectangle.area)
print(rectangle.perimeter)
        

# Задание 5
# Создайте класс BankAccount.
# Внутри храните owner и balance.
# Добавьте методы deposit(amount) и withdraw(amount).
# deposit увеличивает баланс.
# withdraw уменьшает баланс, если денег достаточно.
'''
# TODO: решение
print(" ")
print("№5")
class BankAccount:
    def __init__(self, amount, owner, balance):
        self.owner=owner
        self.balance=balance
        self.amount=amount

    def deposit(amount):
        print(amount.balance + amount)

    def withdraw(amount):
        print(amount.balance + amount)

bank_account = BankAccount('Ivan',1000,0)

bank_account.deposit()
bank_account.withdraw()

amount=int(input('напишите, сколько вы хотите положить/ потратить(через минус): '))

print(bank_account.deposit)
print(bank_account.withdraw)
'''

# Задание 6
# Создайте несколько объектов Student и положите их в список.
# С помощью цикла выведите информацию о каждом студенте.


# TODO: решение
print(" ")
print("№6")
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Anna", 18)
student = Student("Petia", 17)
student = Student("Vova", 16)
student  = Student("Sveta", 18)
n=0
while student<3:
    print(student.name)
    print(student.age)
    n+1