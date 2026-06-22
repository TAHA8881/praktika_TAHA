"""
Этап 05. Экран каталога

Цель: создать полноценный экран каталога товаров с поиском, фильтрами,
выбором товара и добавлением в корзину.
"""


# Задание 1
# Создайте CatalogFrame.
# Он должен получать сервис каталога и корзину через __init__.


# TODO: создать экран каталога


import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# Вспомогательные заглушки (заменятся на реальные сервисы)
# ============================================================

class FakeProduct:
    def __init__(self, id, name, category_id, price, color, description, is_active, sizes=None):
        self.id = id
        self.product_name = name
        self.category_id = category_id
        self.price = price
        self.color = color
        self.description = description
        self.is_active = is_active
        self.sizes = sizes or []  # список доступных размеров

class FakeCatalogService:
    def __init__(self):
        # Тестовые товары с размерами
        self.products = [
            FakeProduct(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True, ["40", "41", "42", "43"]),
            FakeProduct(2, "Платье", 2, 3500, "красный", "Вечернее", True, ["XS", "S", "M", "L"]),
            FakeProduct(3, "Ботинки", 1, 4500, "черный", "Кожаные", True, ["41", "42", "43"]),
            FakeProduct(4, "Сумка", 3, 1200, "коричневый", "Кожаная", True, ["ONE"]),
            FakeProduct(5, "Ремень", 3, 800, "черный", "Кожаный", False, ["M", "L"]),
            FakeProduct(6, "Куртка", 2, 5500, "синий", "Демисезонная", True, ["S", "M", "L", "XL"]),
        ]
        self.categories = [
            {"id": 1, "name": "Обувь"},
            {"id": 2, "name": "Одежда"},
            {"id": 3, "name": "Аксессуары"},
        ]
        self.colors = sorted(set(p.color for p in self.products if p.is_active))
        self.sizes = sorted(set(s for p in self.products for s in p.sizes))

    def get_active_products(self):
        return [p for p in self.products if p.is_active]

    def search_products(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.get_active_products() if keyword in p.product_name.lower()]

    def filter_by_category(self, category_id):
        return [p for p in self.get_active_products() if p.category_id == category_id]

    def filter_by_color(self, color):
        return [p for p in self.get_active_products() if p.color.lower() == color.lower()]

    def filter_by_size(self, size):
        return [p for p in self.get_active_products() if size in p.sizes]

    def filter_by_price_range(self, min_price, max_price):
        return [p for p in self.get_active_products() if min_price <= p.price <= max_price]

    def get_categories(self):
        return self.categories

    def get_colors(self):
        return self.colors

    def get_sizes(self):
        return self.sizes

class FakeCartService:
    def __init__(self):
        self.items = []  # список словарей: {product_id, size, quantity, price}

    def add_to_cart(self, product_id, size, quantity, price):
        # Проверка остатка – заглушка (всегда доступно)
        for item in self.items:
            if item["product_id"] == product_id and item["size"] == size:
                item["quantity"] += quantity
                return
        self.items.append({
            "product_id": product_id,
            "size": size,
            "quantity": quantity,
            "price": price
        })

    def get_cart_items(self):
        return self.items

    def clear_cart(self):
        self.items.clear()

    def is_empty(self):
        return len(self.items) == 0


# ============================================================
# Основной класс экрана каталога
# ============================================================

class CatalogFrame(ttk.Frame):
    def __init__(self, parent, catalog_service, cart_service):
        """
        Задание 1: экран получает сервисы через __init__.
        """
        super().__init__(parent)
        self.catalog_service = catalog_service
        self.cart_service = cart_service

        # Переменные для фильтров
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Все категории")
        self.color_var = tk.StringVar(value="Все цвета")
        self.size_var = tk.StringVar(value="Все размеры")
        self.price_min_var = tk.IntVar(value=0)
        self.price_max_var = tk.IntVar(value=10000)

        # Переменные для деталей выбранного товара
        self.selected_product_id = None
        self.selected_size_var = tk.StringVar()
        self.selected_quantity_var = tk.IntVar(value=1)

        # Словарь для связи идентификатора строки с ID товара
        self.row_to_product = {}

        # Построение интерфейса
        self._build_ui()

        # Загрузка данных
        self.refresh_products()

    def _build_ui(self):
        # ===== Верхняя панель фильтров =====
        filter_frame = ttk.LabelFrame(self, text="Фильтры", padding=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Поиск
        ttk.Label(filter_frame, text="Поиск:").grid(row=0, column=0, padx=5, sticky="w")
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=25)
        self.search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(filter_frame, text="Найти", command=self.on_search).grid(row=0, column=2, padx=5)

        # Категория
        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=3, padx=5, sticky="w")
        categories = ["Все категории"] + [cat["name"] for cat in self.catalog_service.get_categories()]
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                           values=categories, state="readonly", width=12)
        self.category_combo.grid(row=0, column=4, padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_search)

        # Цвет
        ttk.Label(filter_frame, text="Цвет:").grid(row=0, column=5, padx=5, sticky="w")
        colors = ["Все цвета"] + self.catalog_service.get_colors()
        self.color_combo = ttk.Combobox(filter_frame, textvariable=self.color_var,
                                        values=colors, state="readonly", width=10)
        self.color_combo.grid(row=0, column=6, padx=5)
        self.color_combo.bind("<<ComboboxSelected>>", self.on_search)

        # Размер
        ttk.Label(filter_frame, text="Размер:").grid(row=0, column=7, padx=5, sticky="w")
        sizes = ["Все размеры"] + self.catalog_service.get_sizes()
        self.size_combo = ttk.Combobox(filter_frame, textvariable=self.size_var,
                                       values=sizes, state="readonly", width=8)
        self.size_combo.grid(row=0, column=8, padx=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.on_search)

        # Диапазон цен (две колонки)
        ttk.Label(filter_frame, text="Цена от:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.price_min_entry = ttk.Entry(filter_frame, textvariable=self.price_min_var, width=8)
        self.price_min_entry.grid(row=1, column=1, padx=5, sticky="w")
        ttk.Label(filter_frame, text="до:").grid(row=1, column=2, padx=5, sticky="w")
        self.price_max_entry = ttk.Entry(filter_frame, textvariable=self.price_max_var, width=8)
        self.price_max_entry.grid(row=1, column=3, padx=5, sticky="w")
        ttk.Button(filter_frame, text="Применить цену", command=self.on_search).grid(row=1, column=4, padx=5)

        # Кнопка сброса фильтров
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=1, column=5, padx=5, columnspan=3)

        filter_frame.columnconfigure(1, weight=1)

        # ===== Основная область: таблица и детали =====
        main_paned = ttk.PanedWindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=10, pady=5)

        # Левая часть: таблица
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)

# Задание 2
# Добавьте Treeview для списка товаров.
# Показывайте название, категорию, цену, цвет и признак наличия.


# TODO: добавить таблицу каталога

        self.tree = ttk.Treeview(left_frame, columns=("id", "name", "category", "price", "color", "has_stock"),
                                 show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена, руб.")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("has_stock", text="В наличии")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("category", width=100)
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("color", width=80)
        self.tree.column("has_stock", width=80, anchor="center")

        scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")


# Задание 3
# Добавьте метод refresh_products().
# Он должен очищать таблицу и заново заполнять ее товарами из сервиса.


# TODO: добавить обновление таблицы товаров


# Задание 4
# Добавьте поиск по названию и фильтры по категории, цвету и размеру.
# Фильтр по размеру должен использовать сервис, а не проверять остатки в GUI.


# TODO: добавить поиск и фильтры каталога


# Задание 5
# Добавьте выбор строки в таблице.
# При выборе товара покажите его детали в отдельной области.


# TODO: добавить детали выбранного товара

        self.tree.bind("<<TreeviewSelect>>", self.on_product_selected)

        # Правая часть: детали товара
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)

        ttk.Label(right_frame, text="Детали товара", font=("Arial", 12)).pack(pady=5)

        self.details_frame = ttk.LabelFrame(right_frame, text="Информация", padding=5)
        self.details_frame.pack(fill="x", padx=5, pady=5)

        self.details_label = ttk.Label(self.details_frame, text="Выберите товар в таблице", justify="left")
        self.details_label.pack(anchor="w", padx=5, pady=5)

# Задание 6
# Добавьте выбор размера и количества.
# Количество можно вводить через Entry или выбирать через Spinbox.


# TODO: добавить выбор размера и количества

        size_frame = ttk.Frame(right_frame)
        size_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(size_frame, text="Размер:").pack(side="left", padx=5)
        self.size_combo_details = ttk.Combobox(size_frame, textvariable=self.selected_size_var,
                                               state="readonly", width=10)
        self.size_combo_details.pack(side="left", padx=5)

        ttk.Label(size_frame, text="Кол-во:").pack(side="left", padx=5)
        self.quantity_spinbox = ttk.Spinbox(size_frame, textvariable=self.selected_quantity_var,
                                            from_=1, to=10, width=5)
        self.quantity_spinbox.pack(side="left", padx=5)

# Задание 7
# Добавьте кнопку "Добавить в корзину".
# Обработайте ошибки: товар не выбран, размер не выбран, количество некорректно,
# товара недостаточно на складе.


# TODO: добавить товар в корзину через сервис или объект корзины

        self.add_button = ttk.Button(right_frame, text="Добавить в корзину", command=self.add_to_cart)
        self.add_button.pack(pady=10)

        # Статусная строка (можно передать извне, но для теста сделаем свою)
        self.status_var = tk.StringVar(value="Готово")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    # ============================================================
    # Задание 3: метод обновления таблицы
    # ============================================================

    def refresh_products(self):
        """Очищает таблицу и заполняет её товарами из сервиса с учётом фильтров."""
        # Очищаем таблицу и словарь
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)
        self.row_to_product.clear()

        # Получаем товары с учётом фильтров
        products = self._get_filtered_products()

        # Заполняем таблицу
        for product in products:
            # Определяем наличие (хотя бы один размер)
            has_stock = "Да" if product.sizes else "Нет"
            # Ищем категорию
            cat_name = next((cat["name"] for cat in self.catalog_service.get_categories()
                             if cat["id"] == product.category_id), "")
            row_id = self.tree.insert("", "end", values=(
                product.id,
                product.product_name,
                cat_name,
                product.price,
                product.color,
                has_stock
            ))
            self.row_to_product[row_id] = product.id

        # Обновляем статус
        self.status_var.set(f"Найдено товаров: {len(products)}")

        # Сбрасываем выбор
        self.selected_product_id = None
        self.details_label.config(text="Выберите товар в таблице")
        self.size_combo_details.set("")
        self.selected_quantity_var.set(1)

    def _get_filtered_products(self):
        """Применяет все фильтры к списку товаров."""
        # Начинаем с активных товаров
        products = self.catalog_service.get_active_products()

        # Поиск по названию
        search_text = self.search_var.get().strip()
        if search_text:
            products = [p for p in products if search_text.lower() in p.product_name.lower()]

        # Категория
        cat_name = self.category_var.get()
        if cat_name != "Все категории":
            cat_id = next((cat["id"] for cat in self.catalog_service.get_categories()
                           if cat["name"] == cat_name), None)
            if cat_id is not None:
                products = [p for p in products if p.category_id == cat_id]

        # Цвет
        color = self.color_var.get()
        if color != "Все цвета":
            products = [p for p in products if p.color.lower() == color.lower()]

        # Размер
        size = self.size_var.get()
        if size != "Все размеры":
            products = [p for p in products if size in p.sizes]

        # Цена
        try:
            min_price = self.price_min_var.get()
            max_price = self.price_max_var.get()
            if min_price >= 0 and max_price >= min_price:
                products = [p for p in products if min_price <= p.price <= max_price]
        except tk.TclError:
            pass  # если введено не число, игнорируем

        return products

    # ============================================================
    # Задание 4: обработчики поиска и фильтров
    # ============================================================

    def on_search(self, event=None):
        """Вызывается при изменении любого фильтра."""
        self.refresh_products()

    def reset_filters(self):
        """Сбрасывает все фильтры к значениям по умолчанию."""
        self.search_var.set("")
        self.category_var.set("Все категории")
        self.color_var.set("Все цвета")
        self.size_var.set("Все размеры")
        self.price_min_var.set(0)
        self.price_max_var.set(10000)
        self.refresh_products()
        self.status_var.set("Фильтры сброшены")

    # ============================================================
    # Задание 5: выбор строки и показ деталей
    # ============================================================

    def on_product_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            self.selected_product_id = None
            self.details_label.config(text="Выберите товар в таблице")
            self.size_combo_details.set("")
            return

        row_id = selected[0]
        product_id = self.row_to_product.get(row_id)
        if product_id is None:
            return

        # Находим товар в каталоге
        product = None
        for p in self.catalog_service.get_active_products():
            if p.id == product_id:
                product = p
                break
        if product is None:
            return

        self.selected_product_id = product_id

        # Обновляем детали
        details_text = f"Название: {product.product_name}\n"
        details_text += f"Цена: {product.price} руб.\n"
        details_text += f"Цвет: {product.color}\n"
        details_text += f"Описание: {product.description}\n"
        details_text += f"Доступные размеры: {', '.join(product.sizes) if product.sizes else 'Нет'}"
        self.details_label.config(text=details_text)

        # Обновляем список размеров
        self.size_combo_details["values"] = product.sizes
        if product.sizes:
            self.size_combo_details.set(product.sizes[0])
        else:
            self.size_combo_details.set("")

        self.status_var.set(f"Выбран товар: {product.product_name}")

    # ============================================================
    # Задание 6 и 7: добавление в корзину с проверками
    # ============================================================

    def add_to_cart(self):
        # Проверка: выбран ли товар
        if self.selected_product_id is None:
            messagebox.showerror("Ошибка", "Товар не выбран.")
            return

        # Получаем товар
        product = None
        for p in self.catalog_service.get_active_products():
            if p.id == self.selected_product_id:
                product = p
                break
        if product is None:
            messagebox.showerror("Ошибка", "Товар не найден.")
            return

        # Проверка: выбран ли размер
        size = self.selected_size_var.get()
        if not size:
            messagebox.showerror("Ошибка", "Размер не выбран.")
            return
        if size not in product.sizes:
            messagebox.showerror("Ошибка", f"Размер {size} недоступен для этого товара.")
            return

        # Проверка: количество
        try:
            quantity = int(self.selected_quantity_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом.")
            return
        if quantity <= 0:
            messagebox.showerror("Ошибка", "Количество должно быть больше нуля.")
            return

        # (Заглушка) проверка остатка – всегда доступно
        # В реальном приложении здесь был бы вызов сервиса остатков
        # if not self.catalog_service.check_stock(product.id, size, quantity):
        #     messagebox.showerror("Ошибка", "Недостаточно товара на складе.")
        #     return

        # Добавляем в корзину
        try:
            self.cart_service.add_to_cart(product.id, size, quantity, product.price)
            self.status_var.set(f"Товар '{product.product_name}' (размер {size}) добавлен в корзину")
            messagebox.showinfo("Успешно", f"Товар '{product.product_name}' добавлен в корзину.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


# Задание 8
# Проверьте сценарии поиска, фильтрации и добавления в корзину.


# TODO: проверить экран каталога

if __name__ == "__main__":
    # Создаём заглушки сервисов
    catalog = FakeCatalogService()
    cart = FakeCartService()

    # Создаём окно
    root = tk.Tk()
    root.title("Магазин одежды - Каталог")
    root.geometry("1000x650")

    # Создаём экран каталога
    catalog_frame = CatalogFrame(root, catalog, cart)
    catalog_frame.pack(fill="both", expand=True)

    root.mainloop()