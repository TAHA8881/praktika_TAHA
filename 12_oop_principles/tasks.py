"""
Тема 12. Основные принципы ООП
"""


# Задание 1. Инкапсуляция
# Создайте класс BankAccount.
# Внутри храните _owner и _balance.
# Добавьте методы:
# deposit(amount)
# withdraw(amount)
# get_balance()
# Нельзя пополнять или снимать сумму меньше или равную 0.
# Нельзя снять больше, чем есть на балансе.


# TODO: решение
print(" ")
print("№1")
class BankAccount:
    def __init__(self, balance, owner):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._owner = owner
        self._balance = balance


    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        if amount > self._balance:
            raise ValueError("Недостаточно средств")

        self._balance -= amount

    def get_balance(self):
        return self._balance


# Задание 2. Инкапсуляция в модели
# Создайте класс Product.
# Внутри храните _title и _price.
# Добавьте метод set_price(price), который меняет цену.
# Цена не может быть отрицательной.
# Добавьте метод get_info(), который возвращает строку с названием и ценой.


# TODO: решение
print(" ")
print("№2")
class Product:
    def __init__(self, title, price):
        if price < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._title = title
        self._price = price

    def set_price(self, price, price_a):
        if price_a != price:
            self.price = price_a
            return self.price

    def get_info(self):
        return self._price, self._title
       


# Задание 3. Наследование
# Создайте класс User с атрибутом name и методом get_role().
# get_role() должен возвращать "user".
# Создайте класс Admin, который наследуется от User.
# Переопределите get_role(), чтобы он возвращал "admin".


# TODO: решение
print(" ")
print("№3")
class User:
    def get_role(self):
        return "user"


class Admin(User):
    def get_role(self):
        return "admin"

# Задание 4. Наследование и расширение поведения
# Создайте класс Employee с атрибутами name и salary.
# Добавьте метод get_info().
# Создайте класс Manager, который наследуется от Employee.
# Добавьте Manager атрибут department.
# Переопределите get_info(), чтобы он возвращал имя, зарплату и отдел.


# TODO: решение
print(" ")
print("№4")
class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._name = name
        self._salary = salary

    def set_price(self, salary, salary_a):
        if salary_a != salary:
            self.salary = salary_a
            return self.salary

class Manager(Employee):
    def get_role(self):
        return "admin"
    
    def department(self,department):
        self.department=department
        return "department"

    def get_info(self):
        return self._salary
        return self._department

# Задание 5. Полиморфизм
# Создайте классы EmailNotifier и SmsNotifier.
# В каждом классе должен быть метод send(message).
# EmailNotifier возвращает строку "Email: <message>".
# SmsNotifier возвращает строку "SMS: <message>".
# Создайте функцию notify(notifier, message), которая вызывает notifier.send(message).
# Проверьте функцию с объектами обоих классов.


# TODO: решение
print(" ")
print("№5")
class EmailNotifier:
    def send(self, message):
        print(f"Email: {message}")


class SmsNotifier:
    def send(self, message):
        print(f"SMS: {message}")


def notify(notifier, message):
    notifier.send(message)


notify(EmailNotifier(), "Заказ создан")
notify(SmsNotifier(), "Заказ создан")

# Задание 6. Абстракция
# Создайте классы MemoryStorage и ConsoleStorage.
# У каждого должен быть метод save(item).
# MemoryStorage сохраняет элементы в список.
# ConsoleStorage выводит элемент на экран.
# Создайте функцию save_item(storage, item), которая вызывает storage.save(item).
# Проверьте функцию с обоими хранилищами.


# TODO: решение
print(" ")
print("№6")
class MemoryStorage:
    def __init__(self):
        self.items = []

    def save(self, item):
        self.items.append(item)


class ConsoleStorage:
    def __init__(self, storages):
        self.storages = storages

    def save(self, item):
        with open(self.storages, "a", encoding="utf-8") as storage:
            storage.write(str(item) + "\n")

    def save_item(storage, item):
        storage.save(item)

# Задание 7. Композиция
# Создайте класс Engine с методом start().
# Метод возвращает "Двигатель запущен".
# Создайте класс Car.
# Внутри Car должен храниться объект Engine.
# Метод Car.start() должен запускать двигатель и возвращать результат.


# TODO: решение
print(" ")
print("№7")
class Engine:
    def start(self):
        return "Двигатель запущен"


class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        return self.engine.start()