"""
Тема 13. Атрибуты класса и атрибуты объекта
"""


# Задание 1
# Создайте класс Course.
# У класса должен быть атрибут класса platform со значением "Stepik".
# В __init__ сохраните title как атрибут объекта.
# Создайте два курса и выведите их названия и platform.


# TODO: решение
print(" ")
print("№1")
class Course:
    def __init__(self, title):
        self.title = title


course1 = Course("Anna")
course2 = Course("Ivan")
platform = "Stepik"

print(course1.title, platform)
print(course2.title, platform)

# Задание 2
# Создайте класс Ticket.
# У класса должен быть атрибут класса currency со значением "руб.".
# В __init__ сохраните event_name и price.
# Добавьте метод get_info(), который возвращает строку:
# Билет на <event_name>: <price> <currency>


# TODO: решение
print(" ")
print("№2")
class Ticket:
    def __init__(self, event_name, price):
        self.event_name = event_name
        self.price = price
    
    def get_info(self):
        print(Ticket.event_name, ":", Ticket.price, Ticket.currency)

    currency = "руб."





# Задание 3
# Создайте класс Visit.
# Добавьте атрибут класса total_visits со значением 0.
# При создании каждого объекта увеличивайте Visit.total_visits на 1.
# Создайте несколько посещений и выведите Visit.total_visits.


# TODO: решение
print(" ")
print("№3")
class Visit:
    count = 0

    def __init__(self, name):
        self.name = name
        Visit.count += 1


visit1 = Visit("Anna")
visit2 = Visit("Ivan")

print(Visit.count)

# Задание 4
# Создайте класс Delivery.
# Добавьте атрибуты класса STATUS_WAITING = "waiting" и STATUS_SENT = "sent".
# При создании доставки status должен быть STATUS_WAITING.
# Добавьте метод send(), который меняет status на STATUS_SENT.


# TODO: решение

print(" ")
print("№4")
class Delivery:
    STATUS_WAITING = "waiting"
    STATUS_SENT = "sent"

    def __init__(self, number):
        self.number = number
        self.status = self.STATUS_WAITING
    
    def send(self):
        return "self.status = self.STATUS_SENT"

# Задание 5
# Создайте класс Laptop.
# У класса должен быть атрибут класса .
# У объекта должны быть model и owner.
# Создайте несколько ноутбуков и покажите, что warranty_months общий для всех.


# TODO: решение
print(" ")
print("№5")
class Laptop:
    WARRANTY_MONTHS = 19
    def __init__(self, model, owner):
        self.model = model
        self.owner = owner
        self.warranty_months = self.WARRANTY_MONTHS

laptop1 = Laptop("IIISI","Anna")
laptop2 = Laptop("Мостех","Ivan")

print(laptop1)
print(laptop2)

# Задание 6
# Создайте класс Message.
# У класса должен быть атрибут total_sent.
# Каждый новый объект увеличивает total_sent.
# Добавьте метод get_total_sent(), который возвращает общее количество созданных сообщений.


# TODO: решение
print(" ")
print("№6")

class Message:
    count = 0

    def __init__(self, name):
        self.name = name
        Message.count += 1

    def get_total_sent(self):
        print(Message.count)

message1 = Message("Anna")
message2 = Message("Ivan")

