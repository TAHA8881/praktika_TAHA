"""
Этап 01. Основы tkinter

Цель: создать первое desktop-окно приложения и познакомиться с базовыми
виджетами tkinter.

На этом этапе не подключайте базу данных и backend из задания 17.
Сначала нужно понять, как работает окно и главный цикл.
"""


# Задание 1
# Импортируйте tkinter и создайте главное окно приложения.
# Задайте заголовок окна и начальный размер.


# TODO: создать главное окно

import tkinter as tk

class DesktopApp:
    def __init__(self):
        # Создаём главное окно
        self.root = tk.Tk()
        self.root.title("Магазин одежды")
        self.root.geometry("500x300")

# Задание 2
# Добавьте в окно заголовок приложения через Label.
# Текст должен быть связан с будущим магазином одежды.


# TODO: добавить Label с названием приложения

        self.title_label = tk.Label(
            self.root,
            text="Добро пожаловать в наш магазин одежды!",
            font=("Arial", 16)
        )
        self.title_label.pack(pady=20)


# Задание 3
# Добавьте несколько кнопок-заглушек:
# "Каталог", "Корзина", "Оформить заказ", "Выход".
# Пока кнопки могут ничего не делать.


# TODO: добавить кнопки главного меню

        self.catalog_btn = tk.Button(self.root, text="Каталог")
        self.catalog_btn.pack(pady=5)

        self.cart_btn = tk.Button(self.root, text="Корзина")
        self.cart_btn.pack(pady=5)

        self.order_btn = tk.Button(self.root, text="Оформить заказ")
        self.order_btn.pack(pady=5)


# Задание 4
# Добавьте обработчик для кнопки "Выход", который закрывает окно.


# TODO: добавить закрытие окна по кнопке

        self.exit_btn = tk.Button(
            self.root,
            text="Выход",
            command=self.close_app
        )
        self.exit_btn.pack(pady=20)

    def close_app(self):
        """Обработчик для кнопки 'Выход' — закрывает окно."""
        self.root.destroy()

    def run(self):
        """Запуск главного цикла приложения."""
        self.root.mainloop()



# Задание 5
# Перепишите код в виде класса DesktopApp.
# У класса должен быть метод run(), который запускает mainloop().


# TODO: оформить первое приложение как класс


# Задание 6
# Запустите файл и проверьте, что окно открывается, кнопки видны,
# а кнопка выхода закрывает приложение.


# TODO: добавить ручную проверку запуска

if __name__ == "__main__":
    app = DesktopApp()
    app.run()
