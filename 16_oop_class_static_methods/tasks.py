"""
Тема 16. classmethod и staticmethod
"""


# Задание 1
# Создайте класс Employee с атрибутами name и position.
# Добавьте обычный метод get_info(), который возвращает строку с именем и должностью.


# TODO: решение
print(" ")
print("№1")
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def get_info(self):
        return f"Пользователь: {self.name}, должность: {self.position}"
    

# Задание 2
# Добавьте в Employee метод класса from_dict(data).
# Он должен создавать сотрудника из словаря:
# {"name": ..., "position": ...}


# TODO: решение
print(" ")
print("№2")
class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["position"])


data = {"name": "Anna", "position": "anna@example.com"}
employee = Employee.from_dict(data)


# Задание 3
# Создайте класс Song с атрибутами title и duration.
# Добавьте метод класса from_string(text).
# Строка приходит в формате:
# title;duration
# Например: "Imagine;183"


# TODO: решение
print(" ")
print("№3")
class Song:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

    @classmethod
    def from_string(cls, text):
        title, duration = text.split(";")
        return cls(title, int(duration))


song = Song.from_string("Book;500")

# Задание 4
# Создайте класс TextHelper.
# Добавьте staticmethod is_short(text), который возвращает True,
# если длина строки меньше 10, и False иначе.
# Проверьте метод без создания объекта.


# TODO: решение
print(" ")
print("№4")
class MathHelper:
    @staticmethod
    def is_short(text):
        if len(text) < 10:
            return "True"
        else:
            return "False"


print(MathHelper.is_short("Статический метод"))


# Задание 5
# Создайте класс Password.
# В __init__ принимайте value.
# Добавьте staticmethod is_strong(value), который проверяет,
# что длина пароля не меньше 8.
# Если пароль слишком короткий, выбрасывайте ValueError.


# TODO: решение
print(" ")
print("№4")
class Password:
    @staticmethod
    def is_strong(value):
        if len(value) >= 8:
            return "Ok"
        else:
            return "ValueError"


print(Password.is_strong("Статический метод"))


# Задание 6
# Создайте класс Time.
# В __init__ принимайте hours и minutes.
# Добавьте classmethod from_string(text).
# Строка приходит в формате:
# "09:30"
# Метод должен вернуть объект Time.
# Добавьте __str__(), чтобы время красиво выводилось через print().


# TODO: решение
print(" ")
print("№4")
class Time:
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

    @classmethod
    def from_string(cls, text):
        hours, minutes = text.split(":")
        return cls(int(hours), int(minutes))
    
    def __str__(self):
        return f"Время: {self.hours}:{self.minutes}"
    
time= Time.from_string("9:30")
print (time)
