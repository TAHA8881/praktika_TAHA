"""
Тема 15. property и сеттеры
"""


# Задание 1
# Создайте класс CourseProgress.
# В __init__ принимайте student_name и percent.
# Храните процент выполнения во внутреннем атрибуте _percent.
# Добавьте property percent, который возвращает _percent.
# Создайте объект и выведите progress.percent.


# TODO: решение
print(" ")
print("№1")
class CourseProgress:
    def __init__(self, student_name, percent):
        self.student_name = student_name
        self._percent = percent

    @property 
    def percent(self):
        return self._percent

course_progress = CourseProgress("Book", 100)
print(course_progress.percent)

# Задание 2
# Добавьте в CourseProgress сеттер для percent.
# Процент не может быть меньше 0 или больше 100.
# В __init__ используйте self.percent = percent, чтобы начальное значение тоже проходило проверку.


# TODO: решение
print(" ")
print("№2")
class CourseProgress:
    def __init__(self, student_name, percent):
        self.student_name = student_name
        self._percent = percent

    @property 
    def percent(self):
        return self._percent
    
    @percent.setter
    def percent(self, value):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")

        self._percent = value

course_progress = CourseProgress("Book", 100)
course_progress.percent = 100
print(course_progress.percent)


# Задание 3
# Создайте класс Passport.
# В __init__ принимайте number.
# Храните номер во внутреннем атрибуте _number.
# Добавьте property number без сеттера.
# Проверьте, что номер можно прочитать через passport.number.


# TODO: решение
print(" ")
print("№3")
class Passport:
    def __init__(self, number):
        self._number = number

    @property 
    def number(self):
        return self._number

passport = Passport(100)
print(passport.number)


# Задание 4
# Создайте класс Circle.
# В __init__ принимайте radius.
# Добавьте property diameter, который возвращает диаметр.
# Добавьте property area, который возвращает площадь круга.
# Для числа pi можно использовать 3.14.


# TODO: решение
print(" ")
print("№4")
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property 
    def diameter(self):
        return 2 * self._radius
    
    @property 
    def area(self):
        return 3.14*self._radius*3.14*self._radius
    
circle = Circle(100)
print(circle.diameter)
print(circle.area)


# Задание 5
# Создайте класс StorageBox.
# Внутри храните _items_count.
# Добавьте property items_count только для чтения.
# Добавьте методы add_items(count) и remove_items(count).
# Нельзя добавлять или убирать количество меньше или равное 0.
# Нельзя убрать больше предметов, чем есть в коробке.


# TODO: решение
print(" ")
print("№5")
class StorageBox:

    count = 0
    def __init__(self, items_count):
        self._items_count = items_count

    @property 
    def items_count(self):
        return self._items_count
    
    def add_items(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        self._items_count += amount

    def remove_items(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        if amount > self._items_count:
            raise ValueError("Недостаточно средств")

        self.__items_count -= amount

    def get__items_count(self):
        return self.__items_count



# Задание 6
# Создайте класс Speed.
# Внутри храните скорость в километрах в час.
# Добавьте property kmh с сеттером.
# Скорость не может быть отрицательной.
# Добавьте property ms, который возвращает скорость в метрах в секунду по формуле:
# kmh / 3.6


# TODO: решение
print(" ")
print("№6")
class Speed:
    def __init__(self, kmh):
        self.kmh = kmh
    
    @property
    def kmh(self):
        return self._kmh

    @kmh.setter
    def kmh(self, value):
        if value < 0:
            raise ValueError("Скорость не может быть отрицательной")

        self._kmh = value

    @property
    def ms(self):
        return self._kmh/3.6


speed = Speed(500)
speed.kmh = 700

print(speed.kmh)
print(speed.ms)