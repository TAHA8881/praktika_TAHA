"""
Тема 11. Классы для интерфейса
"""


# Задание 1
# Создайте модель User с атрибутом name.
# Добавьте метод get_greeting(), который возвращает приветствие.
# Важно: внутри User нельзя использовать input() и print().


# TODO: решение
print(" ")
print("№1")
class User:
    def __init__(self, name):
        self.name = name

    def get_greeting(self):
        return f"Привет, {self.name}"

user = User("Ivan") 

user.get_greeting()
print(user.get_greeting())

# Задание 2
# Создайте класс ConsoleUserInterface.
# Добавьте метод ask_name(), который спрашивает имя через input().
# Добавьте метод show_message(message), который выводит сообщение через print().


# TODO: решение
print(" ")
print("№2")
class ConsoleUserInterface:
    def ask_name(self):
        return input("Введите имя: ")

    def show_message(self, message):
        print(message)

console_user_interface=ConsoleUserInterface()
message = "Hi!"
console_user_interface.ask_name()
console_user_interface.show_message(message)


# Задание 3
# Создайте класс App.
# В __init__ он должен принимать interface.
# В методе run() он должен:
# 1. спросить имя через interface;
# 2. создать User;
# 3. показать приветствие через interface.


# TODO: решение
print(" ")
print("№3")
class App:
    def __init__(self, interface):
        self.interface = interface

    def run(self):
        name = self.interface.ask_name()
        user = User(name)
        self.interface.show_message(user.get_greeting())    
        
interface = ConsoleUserInterface()
app = App(interface)
app.run()




# Задание 4
# Создайте модель Task.
# Атрибуты: title, is_done.
# Добавьте метод mark_done().
# Создайте интерфейс ConsoleTaskInterface с методами:
# ask_task_title(), show_task(task).


# TODO: решение
print(" ")
print("№4")
class Task:
    def __init__(self, title):
        self.title = title
        self.is_done = False

    def mark_done(self):
        self.is_done = True

class ConsoleTaskInterface:
    def ask_task_title(self):
        return input("Название задачи: ")

    def show_task(self, task):
        status = "готово" if task.is_done else "не готово"
        print(f"{task.title}: {status}")

# Задание 5
# Создайте класс TaskApp.
# Он должен хранить список задач.
# Через интерфейс он должен уметь добавить задачу и показать все задачи.
# Пока можно без бесконечного меню: просто вызовите методы вручную.

'''
# TODO: решение
print(" ")
print("№5")

class TaskApp:
    def __init__(self, task):
 #       self.interface = interface
        self.task = task

  #  def run(self):
  #      task = self.interface.ask_task()
  #      user = User(task)


    def task_spisok(self, task, zadacha):
        task = []

        if a == 1:
            zadacha = input("Выведите задачу: ")
            task.append(zadacha)
        elif a == 2:
            self.task.append(task)
        else:
            print("error")
a =int(input("Выведите 1, если хотите добавить задачу. Введите 2, если хотите показать все задачи: "))
'''

# Задание 6
# Создайте класс Menu.
# Метод show() выводит пункты:
# 1. Добавить задачу
# 2. Показать задачи
# 0. Выход
# Метод ask_choice() возвращает выбор пользователя.
# Подумайте, как этот класс можно использовать внутри TaskApp.


# TODO: решение

class TaskApp:
    def __init__(self, task):
        self.task = task

    def add_task(self, task):
        task = []
        self.task.append(task)

    def show_tasks(self,):
        print(self.task)
class ConsoleUserInterface:
    def ask_name(self):
        return input("Введите имя: ")

    def show_message(self, message):
        print(message)

class Menu:
    def show(self):
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("0. Выход")

    def ask_choice(self):
        return input("Выберите пункт: ")
    
    def run(self):
        a = self.menu.ask_choice()
        if a == '1':
            self.add_task()
        elif a == '2':
            self.show_tasks()



    