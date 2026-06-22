"""
Этап 02. Компоновка и виджеты

Цель: научиться размещать элементы интерфейса и использовать базовые
ttk-виджеты для будущего desktop-приложения магазина.
"""


# Задание 1
# Создайте главное окно и разделите его на несколько областей через Frame:
# верхняя панель, основная область, нижняя панель.


# TODO: создать структуру окна через Frame

import tkinter as tk
from tkinter import ttk


class StoreApp:
    def __init__(self):
        # ===== Задание 1: создаём главное окно и делим его на области =====
        self.root = tk.Tk()
        self.root.title("Магазин одежды - Каталог")
        self.root.geometry("800x500")

        # Настройка растяжения главного окна
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)  # основная область (таблица) будет растягиваться

        # Верхняя панель (поиск + фильтры)
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Основная область (таблица)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Нижняя панель (действия)
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)


# Задание 2
# В верхнюю панель добавьте поле поиска Entry и кнопку "Найти".


# TODO: добавить панель поиска

        self.search_label = ttk.Label(self.top_frame, text="Поиск:")
        self.search_label.grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.search_entry = ttk.Entry(self.top_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")

        self.search_btn = ttk.Button(self.top_frame, text="Найти", command=self.search_products)
        self.search_btn.grid(row=0, column=2, padx=(0, 20))


# Задание 3
# Добавьте Combobox для выбора категории.
# На этом этапе можно использовать тестовый список категорий.


# TODO: добавить выбор категории

        self.category_label = ttk.Label(self.top_frame, text="Категория:")
        self.category_label.grid(row=0, column=3, padx=(0, 5), sticky="w")

        # Тестовые категории
        self.categories = ["Все категории", "Обувь", "Одежда", "Аксессуары"]
        self.category_box = ttk.Combobox(
            self.top_frame,
            values=self.categories,
            state="readonly",
            width=15
        )
        self.category_box.set("Все категории")
        self.category_box.grid(row=0, column=4, padx=(0, 10))

        # Настройка растяжения для верхней панели
        self.top_frame.columnconfigure(1, weight=1)


# Задание 4
# В основной области создайте Treeview для отображения товаров.
# Добавьте колонки: название, категория, цена, цвет, активность.


# TODO: добавить таблицу товаров

        self.columns = ("id", "name", "category", "price", "color", "is_active")
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=self.columns,
            show="headings",
            height=15
        )

        # Заголовки колонок
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена, руб.")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("is_active", text="Активен")

        # Ширина колонок
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("color", width=100, anchor="w")
        self.tree.column("is_active", width=80, anchor="center")

        # Полоса прокрутки
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Размещаем таблицу и скроллбар
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")


# Задание 5
# Заполните таблицу несколькими тестовыми строками без подключения к базе данных.


# TODO: добавить тестовые строки в таблицу

        self.add_test_data()

# Задание 6
# В нижнюю панель добавьте кнопки "Добавить в корзину" и "Очистить фильтры".


# TODO: добавить нижнюю панель действий

        self.add_to_cart_btn = ttk.Button(
            self.bottom_frame,
            text="Добавить в корзину",
            command=self.add_to_cart
        )
        self.add_to_cart_btn.pack(side="left", padx=5)

        self.clear_filters_btn = ttk.Button(
            self.bottom_frame,
            text="Очистить фильтры",
            command=self.clear_filters
        )
        self.clear_filters_btn.pack(side="left", padx=5)

    def add_test_data(self):
        """Задание 5: заполняем таблицу тестовыми данными."""
        test_products = [
            (1, "Кроссовки", "Обувь", 2500, "белый", "Да"),
            (2, "Платье", "Одежда", 3500, "красный", "Да"),
            (3, "Ботинки", "Обувь", 4500, "черный", "Да"),
            (4, "Сумка", "Аксессуары", 1200, "коричневый", "Да"),
            (5, "Ремень", "Аксессуары", 800, "черный", "Нет"),
            (6, "Куртка", "Одежда", 5500, "синий", "Да"),
            (7, "Шарф", "Аксессуары", 500, "серый", "Да"),
            (8, "Сапоги", "Обувь", 6800, "бежевый", "Нет"),
        ]
        for product in test_products:
            self.tree.insert("", "end", values=product)

    # ===== Заглушки для команд =====
    def search_products(self):
        """Заглушка для поиска."""
        search_text = self.search_entry.get().strip()
        print(f"Поиск: {search_text}")  # пока просто вывод в консоль

    def add_to_cart(self):
        """Заглушка для добавления в корзину."""
        print("Добавление в корзину")

    def clear_filters(self):
        """Очистка фильтров."""
        self.search_entry.delete(0, tk.END)
        self.category_box.set("Все категории")
        print("Фильтры очищены")

    def run(self):
        """Запуск главного цикла."""
        self.root.mainloop()


# Задание 7
# Проверьте, что при изменении размера окна таблица растягивается,
# а кнопки и поля остаются читаемыми.


# TODO: проверить поведение окна при изменении размера


if __name__ == "__main__":
    app = StoreApp()
    app.run()