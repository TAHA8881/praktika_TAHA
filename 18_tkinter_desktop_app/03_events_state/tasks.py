"""
Этап 03. События и состояние

Цель: добавить обработчики действий пользователя, переменные интерфейса
и обновление окна после событий.
"""


# Задание 1
# Создайте окно с полем поиска, выпадающим списком категории и таблицей товаров.
# Можно использовать код из предыдущего этапа.


# TODO: подготовить экран с тестовыми товарами


import tkinter as tk
from tkinter import ttk, messagebox


class StoreApp:
    def __init__(self):
        # ========== Задание 1: окно с тестовыми товарами ==========
        self.root = tk.Tk()
        self.root.title("Магазин одежды - Каталог")
        self.root.geometry("800x550")

        # Настройка растяжения главного окна
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Верхняя панель (поиск + категории)
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Основная область (таблица)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Нижняя панель (кнопки)
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Строка статуса
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))


# Задание 2
# Создайте StringVar для поисковой строки и выбранной категории.
# Свяжите их с Entry и Combobox.


# TODO: добавить переменные интерфейса

        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Все категории")
        self.selected_product_id = None  # сохраняем выбранный ID

        # ========== Поисковая строка ==========
        ttk.Label(self.top_frame, text="Поиск:").grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.search_entry = ttk.Entry(self.top_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.search_btn = ttk.Button(self.top_frame, text="Найти", command=self.on_search)
        self.search_btn.grid(row=0, column=2, padx=(0, 20))

        # ========== Категории ==========
        ttk.Label(self.top_frame, text="Категория:").grid(row=0, column=3, padx=(0, 5), sticky="w")
        self.category_box = ttk.Combobox(
            self.top_frame,
            textvariable=self.category_var,
            values=["Все категории", "Обувь", "Одежда", "Аксессуары"],
            state="readonly",
            width=15
        )
        self.category_box.grid(row=0, column=4, padx=(0, 10))
        self.category_box.bind("<<ComboboxSelected>>", self.on_search)  # перезапускаем поиск при смене категории

        self.top_frame.columnconfigure(1, weight=1)

        # ========== Таблица ==========
        self.columns = ("id", "name", "category", "price", "color", "is_active")
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=self.columns,
            show="headings",
            height=15
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена, руб.")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("is_active", text="Активен")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("color", width=100, anchor="w")
        self.tree.column("is_active", width=80, anchor="center")

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # ========== Тестовые данные ==========
        self.products = [
            (1, "Кроссовки", "Обувь", 2500, "белый", "Да"),
            (2, "Платье", "Одежда", 3500, "красный", "Да"),
            (3, "Ботинки", "Обувь", 4500, "черный", "Да"),
            (4, "Сумка", "Аксессуары", 1200, "коричневый", "Да"),
            (5, "Ремень", "Аксессуары", 800, "черный", "Нет"),
            (6, "Куртка", "Одежда", 5500, "синий", "Да"),
            (7, "Шарф", "Аксессуары", 500, "серый", "Да"),
            (8, "Сапоги", "Обувь", 6800, "бежевый", "Нет"),
        ]
        self.display_products(self.products)

# Задание 3
# Добавьте обработчик кнопки "Найти".
# Он должен читать текст поиска и обновлять таблицу тестовых товаров.


# TODO: добавить поиск по тестовым данным

  # метод on_search уже привязан выше

# Задание 4
# Добавьте обработчик выбора строки в Treeview.
# Сохраняйте выбранный товар в атрибуте приложения.


# TODO: сохранить выбранный товар

        self.tree.bind("<<TreeviewSelect>>", self.on_product_selected)


# Задание 5
# Добавьте кнопку "Добавить в корзину".
# Если товар не выбран, покажите ошибку через messagebox.
# Если выбран, покажите информационное сообщение.


# TODO: добавить обработчик кнопки добавления

        self.add_to_cart_btn = ttk.Button(
            self.bottom_frame,
            text="Добавить в корзину",
            command=self.add_to_cart
        )
        self.add_to_cart_btn.pack(side="left", padx=5)

        # Дополнительная кнопка для очистки поиска
        self.clear_btn = ttk.Button(
            self.bottom_frame,
            text="Очистить фильтры",
            command=self.clear_filters
        )
        self.clear_btn.pack(side="left", padx=5)

# Задание 6
# Добавьте строку статуса внизу окна.
# Обновляйте ее после поиска, выбора товара и добавления в корзину.


# TODO: добавить статус приложения

        self.status_var = tk.StringVar(value="Готово")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, anchor="w")
        self.status_label.pack(fill="x")

# Задание 7
# Проверьте несколько сценариев:
# пустой поиск, поиск без результатов, выбор строки, клик без выбранного товара.


# TODO: проверить события и сообщения


        # Все сценарии будут проверены вручную, но базовые уже реализованы
        # - пустой поиск: показывает все товары
        # - поиск без результатов: таблица очищается, статус сообщает об этом
        # - выбор строки: сохраняется ID и обновляется статус
        # - клик без выбранного: показывает ошибку через messagebox

    # ==================================================================
    # Методы работы с таблицей
    # ==================================================================

    def display_products(self, product_list):
        """Отображает переданный список товаров в таблице."""
        # Очищаем таблицу
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)

        # Заполняем
        for product in product_list:
            self.tree.insert("", "end", values=product)

    def get_filtered_products(self):
        """Возвращает список товаров, отфильтрованных по поиску и категории."""
        search_text = self.search_var.get().strip().lower()
        category = self.category_var.get()

        filtered = []
        for p in self.products:
            name = p[1].lower()
            prod_cat = p[2]

            # Фильтр по категории
            if category != "Все категории" and prod_cat != category:
                continue

            # Фильтр по поиску (по названию)
            if search_text and search_text not in name:
                continue

            filtered.append(p)

        return filtered

    # ==================================================================
    # Обработчики событий
    # ==================================================================

    def on_search(self, event=None):
        """Обработчик поиска — обновляет таблицу и статус."""
        filtered = self.get_filtered_products()
        self.display_products(filtered)

        if not filtered:
            self.status_var.set("Ничего не найдено")
        else:
            self.status_var.set(f"Найдено товаров: {len(filtered)}")

    def on_product_selected(self, event):
        """Обработчик выбора строки в таблице."""
        selected = self.tree.selection()
        if selected:
            row_id = selected[0]
            values = self.tree.item(row_id, "values")
            # values: (id, name, category, price, color, is_active)
            self.selected_product_id = int(values[0])
            self.status_var.set(f"Выбран товар: {values[1]} (ID {values[0]})")
        else:
            self.selected_product_id = None

    def add_to_cart(self):
        """Обработчик кнопки 'Добавить в корзину'."""
        if self.selected_product_id is None:
            messagebox.showerror("Ошибка", "Не выбран товар для добавления.")
            self.status_var.set("Ошибка: товар не выбран")
            return

        # Находим товар по ID
        product = None
        for p in self.products:
            if p[0] == self.selected_product_id:
                product = p
                break

        if product is None:
            messagebox.showerror("Ошибка", "Выбранный товар не найден.")
            return

        # Успешное добавление
        messagebox.showinfo("Успешно", f"Товар '{product[1]}' добавлен в корзину!")
        self.status_var.set(f"Добавлен в корзину: {product[1]}")

    def clear_filters(self):
        """Очистка полей поиска и категории."""
        self.search_var.set("")
        self.category_var.set("Все категории")
        self.display_products(self.products)
        self.status_var.set("Фильтры очищены")
        self.selected_product_id = None

    def run(self):
        self.root.mainloop()


# ======================================================================
# Запуск приложения
# ======================================================================

if __name__ == "__main__":
    app = StoreApp()
    app.run()