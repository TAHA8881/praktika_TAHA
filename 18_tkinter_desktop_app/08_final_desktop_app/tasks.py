"""
Этап 08. Итоговое desktop-приложение

Цель: собрать единое tkinter-приложение магазина одежды, которое использует
backend из задания 17 и позволяет пройти путь от каталога до заказа.
"""


# Задание 1
# Создайте финальный класс ClothingStoreDesktopApp.
# Он должен создавать главное окно, настраивать стиль и собирать зависимости.


# TODO: создать финальный класс приложения

import tkinter as tk
from tkinter import ttk, messagebox

BACKEND_AVAILABLE = False

try:
    from importlib import import_module
    from pathlib import Path
    import sys

    # Добавляем путь к проекту (если нужно)
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.append(str(PROJECT_ROOT))

    # Импортируем доменные модели
    domain = import_module("17_clothing_store_project.01_domain_models.tasks")
    Product = domain.Product
    Category = domain.Category
    LeftSizes = domain.LeftSizes
    Byer = domain.Byer

    # Репозитории
    repos = import_module("17_clothing_store_project.03_repositories.tasks")
    CategoryRepository = repos.CategoryRepository
    ProductRepository = repos.ProductRepository
    SizesRepository = repos.SizesRepository
    ByerRepository = repos.ByerRepository
    get_connection = repos.get_connection

    # Сервисы
    catalog_mod = import_module("17_clothing_store_project.04_catalog_service.tasks")
    CatalogService = catalog_mod.CatalogService

    cart_mod = import_module("17_clothing_store_project.05_cart.tasks")
    CartService = cart_mod.CartService

    order_mod = import_module("17_clothing_store_project.06_orders.tasks")
    OrderRepository = order_mod.OrderRepository
    OrderService = order_mod.OrderService

    promo_mod = import_module("17_clothing_store_project.07_promocodes.tasks")
    PromoCodeRepository = promo_mod.PromoCodeRepository
    DiscountService = promo_mod.DiscountService
    AddressRepository = promo_mod.AddressRepository
    Address = promo_mod.Address
    PromoCode = promo_mod.PromoCode

    # Пытаемся импортировать расширенный сервис заказов со скидками
    try:
        OrderServiceWithDiscount = promo_mod.OrderServiceWithDiscount
    except AttributeError:
        OrderServiceWithDiscount = OrderService

    BACKEND_AVAILABLE = True
    print("✅ Реальный backend из задания 17 успешно загружен.")

except Exception as e:
    print(f"⚠️ Реальный backend не найден ({e}), используются заглушки.")
    BACKEND_AVAILABLE = False



# Задание 2
# Подключите backend из задания 17:
# модели, репозитории, сервис каталога, корзину, сервис заказов и скидок.
# Не копируйте код backend-слоя в это задание.


# TODO: подключить backend из задания 17


if not BACKEND_AVAILABLE:

    class FakeProduct:
        def __init__(self, id, name, category_id, price, color, description, is_active, sizes=None):
            self.id = id
            self.product_name = name
            self.category_id = category_id
            self.price = price
            self.color = color
            self.description = description
            self.is_active = is_active
            self.sizes = sizes or []

    class FakeCategory:
        def __init__(self, category_id, category_name, category_description=""):
            self.category_id = category_id
            self.category_name = category_name
            self.category_description = category_description

    class FakeLeftSizes:
        def __init__(self, store_id, product_id, size, quantity):
            self.store_id = store_id
            self.product_id = product_id
            self.size = size
            self.quantity = quantity

    class FakeByer:
        def __init__(self, byer_id, byer_name, byer_email, byer_telephone):
            self.byer_id = byer_id
            self.byer_name = byer_name
            self.byer_email = byer_email
            self.byer_telephone = byer_telephone

    # Заглушки репозиториев и сервисов
    class FakeCategoryRepository:
        def get_all(self):
            return [
                FakeCategory(1, "Обувь"),
                FakeCategory(2, "Одежда"),
                FakeCategory(3, "Аксессуары")
            ]
        def get_by_id_c(self, cat_id):
            for c in self.get_all():
                if c.category_id == cat_id:
                    return c
            return None

    class FakeProductRepository:
        def __init__(self):
            self.products = [
                FakeProduct(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True, ["40","41","42","43"]),
                FakeProduct(2, "Платье", 2, 3500, "красный", "Вечернее", True, ["XS","S","M","L"]),
                FakeProduct(3, "Ботинки", 1, 4500, "черный", "Кожаные", True, ["41","42","43"]),
                FakeProduct(4, "Сумка", 3, 1200, "коричневый", "Кожаная", True, ["ONE"]),
                FakeProduct(5, "Ремень", 3, 800, "черный", "Кожаный", False, ["M","L"]),
            ]

        def get_all(self, only_active=False):
            products = self.products
            if only_active:
                return [p for p in products if p.is_active]
            return products

        def get_by_id_p(self, product_id):
            for p in self.products:
                if p.id == product_id:
                    return p
            return None

        def search_by_name(self, keyword, only_active=False):
            keyword = keyword.lower()
            return [p for p in self.get_all(only_active) if keyword in p.product_name.lower()]

        def filter_by_category(self, cat_id, only_active=False):
            return [p for p in self.get_all(only_active) if p.category_id == cat_id]

        def filter_by_color(self, color, only_active=False):
            color = color.lower()
            return [p for p in self.get_all(only_active) if p.color.lower() == color]

        def filter_by_price_range(self, min_price, max_price, only_active=False):
            return [p for p in self.get_all(only_active) if min_price <= p.price <= max_price]

    class FakeSizesRepository:
        def __init__(self):
            self.stock = {}

        def add_stock(self, product_id, size, quantity):
            self.stock[(product_id, size)] = quantity

        def get_by_product_and_size(self, product_id, size):
            qty = self.stock.get((product_id, size), 0)
            return FakeLeftSizes(1, product_id, size, qty)

        def decrease_quantity(self, product_id, size, amount):
            key = (product_id, size)
            if key in self.stock and self.stock[key] >= amount:
                self.stock[key] -= amount
            else:
                raise ValueError("Недостаточно товара")

    class FakeCartService:
        def __init__(self):
            self.items = []  # list of dict: product_id, name, size, quantity, price
            self._promo = None

        def add_to_cart(self, product_id, size, quantity, price):
            for item in self.items:
                if item["product_id"] == product_id and item["size"] == size:
                    item["quantity"] += quantity
                    return
            self.items.append({
                "product_id": product_id,
                "name": f"Товар {product_id}",
                "size": size,
                "quantity": quantity,
                "price": price
            })

        def remove_item(self, product_id, size):
            self.items = [it for it in self.items if not (it["product_id"] == product_id and it["size"] == size)]

        def update_quantity(self, product_id, size, new_quantity):
            for item in self.items:
                if item["product_id"] == product_id and item["size"] == size:
                    if new_quantity <= 0:
                        self.items.remove(item)
                    else:
                        item["quantity"] = new_quantity
                    return

        def clear_cart(self):
            self.items.clear()
            self._promo = None

        def get_cart_items(self):
            return self.items

        def get_cart_total(self):
            return sum(it["price"] * it["quantity"] for it in self.items)

        def is_empty(self):
            return len(self.items) == 0

        def set_promo_code(self, code):
            self._promo = code

        def get_promo_code(self):
            return self._promo

    class FakeDiscountService:
        def apply_promo(self, total, code):
            if code == "SALE10":
                discount = int(total * 0.1)
                return total - discount, discount
            elif code == "SALE20":
                discount = int(total * 0.2)
                return total - discount, discount
            else:
                raise ValueError("Промокод не найден или недействителен")

    class FakeOrderService:
        def __init__(self):
            self.counter = 0

        def create_order(self, cart_service, customer_data, promo_code=None):
            if cart_service.is_empty():
                raise ValueError("Корзина пуста")
            self.counter += 1
            return {"id": self.counter, "total": cart_service.get_cart_total()}

    # Назначаем заглушки вместо реальных классов
    CategoryRepository = FakeCategoryRepository
    ProductRepository = FakeProductRepository
    SizesRepository = FakeSizesRepository
    ByerRepository = None
    get_connection = lambda: None
    CatalogService = None  # мы будем использовать наш внутренний сервис
    CartService = FakeCartService
    OrderService = FakeOrderService
    DiscountService = FakeDiscountService
    OrderServiceWithDiscount = FakeOrderService
    PromoCodeRepository = None
    AddressRepository = None


# Задание 3
# Добавьте навигацию между экранами:
# каталог, корзина, оформление заказа.


# TODO: добавить навигацию


if CatalogService is None:
    # Используем репозиторий как сервис
    class SimpleCatalogService:
        def __init__(self, prod_repo, cat_repo, size_repo):
            self.prod_repo = prod_repo
            self.cat_repo = cat_repo
            self.size_repo = size_repo

        def get_active_products(self):
            return self.prod_repo.get_all(only_active=True)

        def search_products(self, keyword):
            return self.prod_repo.search_by_name(keyword, only_active=True)

        def filter_by_category(self, cat_id):
            return self.prod_repo.filter_by_category(cat_id, only_active=True)

        def filter_by_color(self, color):
            return self.prod_repo.filter_by_color(color, only_active=True)

        def filter_by_price_range(self, min_p, max_p):
            return self.prod_repo.filter_by_price_range(min_p, max_p, only_active=True)

        def filter_by_size(self, size):
            products = self.prod_repo.get_all(only_active=True)
            result = []
            for p in products:
                stock = self.size_repo.get_by_product_and_size(p.id, size)
                if stock and stock.quantity > 0:
                    result.append(p)
            return result

        def get_categories(self):
            return self.cat_repo.get_all()

        def get_colors(self):
            colors = set()
            for p in self.prod_repo.get_all(only_active=True):
                colors.add(p.color)
            return sorted(colors)

        def get_sizes(self):
            # Для простоты возвращаем фиксированный список
            return ["XS", "S", "M", "L", "XL", "40", "41", "42", "43", "ONE"]

    CatalogService = SimpleCatalogService


# Задание 4
# Подключите CatalogFrame, CartFrame и CheckoutFrame.
# Экраны должны получать нужные сервисы через __init__.


# TODO: подключить экраны приложения


class CatalogFrame(ttk.Frame):
    """Экран каталога товаров."""
    def __init__(self, parent, catalog_service, cart_service):
        super().__init__(parent)
        self.catalog_service = catalog_service
        self.cart_service = cart_service
        self.selected_product_id = None

        # Переменные для фильтров
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Все категории")
        self.color_var = tk.StringVar(value="Все цвета")
        self.size_var = tk.StringVar(value="Все размеры")
        self.price_min_var = tk.IntVar(value=0)
        self.price_max_var = tk.IntVar(value=10000)

        # Словарь для связи row_id и product_id
        self.row_to_product = {}

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # Верхняя панель фильтров
        filter_frame = ttk.LabelFrame(self, text="Фильтры", padding=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Поиск
        ttk.Label(filter_frame, text="Поиск:").grid(row=0, column=0, padx=5, sticky="w")
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=25)
        self.search_entry.grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(filter_frame, text="Найти", command=self.apply_filters).grid(row=0, column=2, padx=5)

        # Категория
        categories = ["Все категории"] + [cat.category_name for cat in self.catalog_service.get_categories()]
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                           values=categories, state="readonly", width=12)
        self.category_combo.grid(row=0, column=4, padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.apply_filters)

        # Цвет
        colors = ["Все цвета"] + self.catalog_service.get_colors()
        self.color_combo = ttk.Combobox(filter_frame, textvariable=self.color_var,
                                        values=colors, state="readonly", width=10)
        self.color_combo.grid(row=0, column=6, padx=5)
        self.color_combo.bind("<<ComboboxSelected>>", self.apply_filters)

        # Размер
        sizes = ["Все размеры"] + self.catalog_service.get_sizes()
        self.size_combo = ttk.Combobox(filter_frame, textvariable=self.size_var,
                                       values=sizes, state="readonly", width=8)
        self.size_combo.grid(row=0, column=8, padx=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.apply_filters)

        # Цена
        ttk.Label(filter_frame, text="Цена от:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(filter_frame, textvariable=self.price_min_var, width=8).grid(row=1, column=1, padx=5, sticky="w")
        ttk.Label(filter_frame, text="до:").grid(row=1, column=2, padx=5, sticky="w")
        ttk.Entry(filter_frame, textvariable=self.price_max_var, width=8).grid(row=1, column=3, padx=5, sticky="w")
        ttk.Button(filter_frame, text="Применить цену", command=self.apply_filters).grid(row=1, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить", command=self.reset_filters).grid(row=1, column=5, padx=5, columnspan=3)

        filter_frame.columnconfigure(1, weight=1)

        # Таблица товаров
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "name", "category", "price", "color", "stock"),
                                 show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена, руб.")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("stock", text="В наличии")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("category", width=100)
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("color", width=80)
        self.tree.column("stock", width=80, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Привязка выбора строки
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Кнопка добавления в корзину
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Добавить выбранный товар в корзину", command=self.add_to_cart).pack(side="left", padx=5)

        # Статусная строка
        self.status_var = tk.StringVar(value="Готово")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    def get_filtered_products(self):
        products = self.catalog_service.get_active_products()
        # Поиск
        search = self.search_var.get().strip()
        if search:
            products = [p for p in products if search.lower() in p.product_name.lower()]
        # Категория
        cat_name = self.category_var.get()
        if cat_name != "Все категории":
            cat = next((c for c in self.catalog_service.get_categories() if c.category_name == cat_name), None)
            if cat:
                products = [p for p in products if p.category_id == cat.category_id]
        # Цвет
        color = self.color_var.get()
        if color != "Все цвета":
            products = [p for p in products if p.color.lower() == color.lower()]
        # Размер
        size = self.size_var.get()
        if size != "Все размеры":
            products = [p for p in products if size in getattr(p, 'sizes', [])]
        # Цена
        try:
            min_p = self.price_min_var.get()
            max_p = self.price_max_var.get()
            if max_p >= min_p:
                products = [p for p in products if min_p <= p.price <= max_p]
        except:
            pass
        return products

    def refresh(self):
        self.apply_filters()

    def apply_filters(self, event=None):
        products = self.get_filtered_products()
        # Очистить таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.row_to_product.clear()

        for p in products:
            # Проверка наличия (есть ли размеры)
            has_stock = "Да" if getattr(p, 'sizes', []) else "Нет"
            cat_name = next((c.category_name for c in self.catalog_service.get_categories()
                             if c.category_id == p.category_id), "")
            row_id = self.tree.insert("", "end", values=(p.id, p.product_name, cat_name, p.price, p.color, has_stock))
            self.row_to_product[row_id] = p.id

        self.status_var.set(f"Найдено товаров: {len(products)}")

    def reset_filters(self):
        self.search_var.set("")
        self.category_var.set("Все категории")
        self.color_var.set("Все цвета")
        self.size_var.set("Все размеры")
        self.price_min_var.set(0)
        self.price_max_var.set(10000)
        self.apply_filters()
        self.status_var.set("Фильтры сброшены")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            row = selected[0]
            self.selected_product_id = self.row_to_product.get(row)
            if self.selected_product_id:
                self.status_var.set(f"Выбран товар ID {self.selected_product_id}")

    def add_to_cart(self):
        if self.selected_product_id is None:
            messagebox.showerror("Ошибка", "Не выбран товар.")
            return

        # Ищем товар
        product = self.catalog_service.prod_repo.get_by_id_p(self.selected_product_id) if hasattr(self.catalog_service, 'prod_repo') else None
        if not product:
            # Попробуем через сервис
            for p in self.catalog_service.get_active_products():
                if p.id == self.selected_product_id:
                    product = p
                    break
        if not product:
            messagebox.showerror("Ошибка", "Товар не найден.")
            return

        # Запрашиваем размер и количество (упрощённо)
        size = tk.simpledialog.askstring("Размер", "Введите размер:", parent=self)
        if not size:
            return
        qty_str = tk.simpledialog.askstring("Количество", "Введите количество:", parent=self)
        if not qty_str:
            return
        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Количество должно быть положительным числом.")
            return

        # Проверка наличия (заглушка)
        # В реальности нужно проверить остатки через sizes_repo
        try:
            self.cart_service.add_to_cart(product.id, size, qty, product.price)
            messagebox.showinfo("Успех", f"Товар '{product.product_name}' добавлен в корзину.")
            self.status_var.set(f"Добавлен в корзину: {product.product_name} x{qty}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


class CartFrame(ttk.Frame):
    def __init__(self, parent, cart_service, catalog_service, on_checkout=None):
        super().__init__(parent)
        self.cart_service = cart_service
        self.catalog_service = catalog_service
        self.on_checkout = on_checkout
        self.selected_item = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ttk.Label(self, text="Корзина", font=("Arial", 14)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("product", "size", "qty", "price", "total"), show="headings")
        self.tree.heading("product", text="Товар")
        self.tree.heading("size", text="Размер")
        self.tree.heading("qty", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")
        self.tree.column("product", width=150)
        self.tree.column("size", width=60)
        self.tree.column("qty", width=60)
        self.tree.column("price", width=80)
        self.tree.column("total", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Изменить кол-во", command=self.change_quantity).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить позицию", command=self.remove_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Очистить корзину", command=self.clear_cart).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Перейти к оформлению", command=self.go_checkout).pack(side="right", padx=5)

        self.total_label = ttk.Label(self, text="Итого: 0 руб.", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=5)

        self.status_var = tk.StringVar(value="Корзина")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        items = self.cart_service.get_cart_items()
        total = 0
        for it in items:
            subtotal = it["price"] * it["quantity"]
            total += subtotal
            self.tree.insert("", "end", values=(it["name"], it["size"], it["quantity"], it["price"], subtotal))
        self.total_label.config(text=f"Итого: {total} руб.")
        self.status_var.set(f"В корзине {len(items)} позиций. Итого: {total} руб.")
        self.selected_item = None

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            row = selected[0]
            values = self.tree.item(row, "values")
            # values: (product_name, size, qty, price, total)
            # Для простоты сохраняем размер и имя, но лучше хранить ID – в нашей заглушке нет ID, поэтому только имя и размер
            self.selected_item = (values[0], values[1])
        else:
            self.selected_item = None

    def change_quantity(self):
        if not self.selected_item:
            messagebox.showerror("Ошибка", "Выберите позицию.")
            return
        name, size = self.selected_item
        # Найти позицию в корзине
        items = self.cart_service.get_cart_items()
        target = None
        for it in items:
            if it["name"] == name and it["size"] == size:
                target = it
                break
        if not target:
            messagebox.showerror("Ошибка", "Позиция не найдена.")
            return

        new_qty_str = tk.simpledialog.askstring("Новое количество", f"Товар: {name}\nРазмер: {size}\nВведите новое количество (0 для удаления):",
                                                initialvalue=str(target["quantity"]), parent=self)
        if new_qty_str is None:
            return
        try:
            new_qty = int(new_qty_str)
            if new_qty < 0:
                raise ValueError
            product_id = target.get("product_id", 0)  # если есть
            self.cart_service.update_quantity(product_id, size, new_qty)
            self.refresh()
            self.status_var.set(f"Количество изменено для {name}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое неотрицательное число.")

    def remove_item(self):
        if not self.selected_item:
            messagebox.showerror("Ошибка", "Выберите позицию.")
            return
        name, size = self.selected_item
        if messagebox.askyesno("Подтверждение", f"Удалить {name} (размер {size})?"):
            items = self.cart_service.get_cart_items()
            for it in items:
                if it["name"] == name and it["size"] == size:
                    self.cart_service.remove_item(it.get("product_id", 0), size)
                    break
            self.refresh()
            self.status_var.set(f"Удалено: {name}")

    def clear_cart(self):
        if self.cart_service.is_empty():
            return
        if messagebox.askyesno("Подтверждение", "Очистить всю корзину?"):
            self.cart_service.clear_cart()
            self.refresh()
            self.status_var.set("Корзина очищена.")

    def go_checkout(self):
        if self.cart_service.is_empty():
            messagebox.showerror("Ошибка", "Корзина пуста.")
            return
        if self.on_checkout:
            self.on_checkout()


class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, cart_service, order_service, discount_service,
                 on_order_success=None, on_back_to_catalog=None):
        super().__init__(parent)
        self.cart_service = cart_service
        self.order_service = order_service
        self.discount_service = discount_service
        self.on_order_success = on_order_success
        self.on_back_to_catalog = on_back_to_catalog

        # Переменные формы
        self.name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.house_var = tk.StringVar()
        self.apartment_var = tk.StringVar()
        self.promo_var = tk.StringVar()

        # Итоговые переменные
        self.subtotal_var = tk.StringVar(value="0 руб.")
        self.discount_var = tk.StringVar(value="0 руб.")
        self.total_var = tk.StringVar(value="0 руб.")
        self.promo_status_var = tk.StringVar(value="Промокод не применён")

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        ttk.Label(self, text="Оформление заказа", font=("Arial", 16)).pack(pady=10)

        main_paned = ttk.PanedWindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=10, pady=5)

        # Левая часть – форма
        left = ttk.Frame(main_paned)
        main_paned.add(left, weight=1)

        ttk.Label(left, text="Данные получателя", font=("Arial", 12)).pack(anchor="w", pady=5)
        form = ttk.Frame(left)
        form.pack(fill="x", padx=5)

        row = 0
        ttk.Label(form, text="Имя*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1
        ttk.Label(form, text="Телефон/email*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.contact_var, width=30).grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1
        ttk.Label(form, text="Город*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.city_var, width=30).grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1
        ttk.Label(form, text="Улица*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.street_var, width=30).grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1
        ttk.Label(form, text="Дом*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.house_var, width=30).grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1
        ttk.Label(form, text="Квартира").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.apartment_var, width=30).grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        form.columnconfigure(1, weight=1)

        # Промокод
        promo_frame = ttk.Frame(left)
        promo_frame.pack(fill="x", padx=5, pady=10)
        ttk.Label(promo_frame, text="Промокод:").pack(side="left", padx=5)
        ttk.Entry(promo_frame, textvariable=self.promo_var, width=20).pack(side="left", padx=5)
        ttk.Button(promo_frame, text="Применить", command=self.apply_promo).pack(side="left", padx=5)
        ttk.Label(left, textvariable=self.promo_status_var, foreground="blue").pack(anchor="w", padx=10)

        # Правая часть – сводка
        right = ttk.Frame(main_paned)
        main_paned.add(right, weight=1)

        ttk.Label(right, text="Состав заказа", font=("Arial", 12)).pack(anchor="w", pady=5)

        self.summary_tree = ttk.Treeview(right, columns=("product", "size", "qty", "price"), show="headings")
        self.summary_tree.heading("product", text="Товар")
        self.summary_tree.heading("size", text="Размер")
        self.summary_tree.heading("qty", text="Кол-во")
        self.summary_tree.heading("price", text="Сумма")
        self.summary_tree.column("product", width=150)
        self.summary_tree.column("size", width=60)
        self.summary_tree.column("qty", width=60)
        self.summary_tree.column("price", width=100)
        self.summary_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Итоги
        total_frame = ttk.Frame(right)
        total_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(total_frame, text="Сумма без скидки:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(total_frame, textvariable=self.subtotal_var).grid(row=0, column=1, sticky="e", padx=5)
        ttk.Label(total_frame, text="Скидка:").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(total_frame, textvariable=self.discount_var, foreground="green").grid(row=1, column=1, sticky="e", padx=5)
        ttk.Label(total_frame, text="Итого:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(total_frame, textvariable=self.total_var, font=("Arial", 12, "bold")).grid(row=2, column=1, sticky="e", padx=5)
        total_frame.columnconfigure(0, weight=1)
        total_frame.columnconfigure(1, weight=1)

        ttk.Button(right, text="Оформить заказ", command=self.place_order).pack(pady=10)

        # Статус
        self.status_var = tk.StringVar(value="Заполните форму")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    def refresh(self):
        items = self.cart_service.get_cart_items()
        for row in self.summary_tree.get_children():
            self.summary_tree.delete(row)
        subtotal = 0
        for it in items:
            total_item = it["price"] * it["quantity"]
            subtotal += total_item
            self.summary_tree.insert("", "end", values=(it["name"], it["size"], it["quantity"], total_item))

        # Применяем промокод, если есть
        promo = self.cart_service.get_promo_code()
        if promo:
            try:
                final, discount = self.discount_service.apply_promo(subtotal, promo)
                self.subtotal_var.set(f"{subtotal} руб.")
                self.discount_var.set(f"-{discount} руб.")
                self.total_var.set(f"{final} руб.")
                self.promo_status_var.set(f"Промокод {promo} применён, скидка {discount} руб.")
            except Exception as e:
                self.cart_service.set_promo_code(None)
                self.promo_var.set("")
                self.promo_status_var.set("Ошибка промокода")
                self.subtotal_var.set(f"{subtotal} руб.")
                self.discount_var.set("0 руб.")
                self.total_var.set(f"{subtotal} руб.")
        else:
            self.subtotal_var.set(f"{subtotal} руб.")
            self.discount_var.set("0 руб.")
            self.total_var.set(f"{subtotal} руб.")
            self.promo_status_var.set("Промокод не применён")

    def apply_promo(self):
        code = self.promo_var.get().strip()
        if not code:
            messagebox.showerror("Ошибка", "Введите код промокода")
            return
        try:
            total = self.cart_service.get_cart_total()
            final, discount = self.discount_service.apply_promo(total, code)
            self.cart_service.set_promo_code(code)
            self.refresh()
            messagebox.showinfo("Успех", f"Промокод применён. Скидка {discount} руб.")
        except Exception as e:
            self.cart_service.set_promo_code(None)
            self.refresh()
            messagebox.showerror("Ошибка", str(e))

    def place_order(self):
        # Проверка корзины
        if self.cart_service.is_empty():
            messagebox.showerror("Ошибка", "Корзина пуста.")
            return

        # Проверка формы
        if not all([self.name_var.get().strip(), self.contact_var.get().strip(),
                    self.city_var.get().strip(), self.street_var.get().strip(),
                    self.house_var.get().strip()]):
            messagebox.showerror("Ошибка", "Заполните все обязательные поля (отмечены *).")
            return

        customer_data = {
            "name": self.name_var.get().strip(),
            "contact": self.contact_var.get().strip(),
            "city": self.city_var.get().strip(),
            "street": self.street_var.get().strip(),
            "house": self.house_var.get().strip(),
            "apartment": self.apartment_var.get().strip()
        }
        promo = self.cart_service.get_promo_code()

        try:
            order = self.order_service.create_order(self.cart_service, customer_data, promo)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        # Успех
        self.cart_service.clear_cart()
        self.cart_service.set_promo_code(None)
        self.promo_var.set("")
        self.refresh()
        messagebox.showinfo("Заказ оформлен", f"Номер заказа: {order['id']}\nСумма: {order['total']} руб.")
        self.status_var.set(f"Заказ №{order['id']} оформлен")
        if self.on_back_to_catalog:
            self.on_back_to_catalog()


# Задание 5
# Сделайте обновление экранов при переходе.
# Например, корзина должна показывать актуальные позиции,
# а оформление заказа - актуальную сумму.


# TODO: добавить обновление экранов при навигации


class ClothingStoreDesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Магазин одежды")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        # Настройка стиля
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("Treeview", rowheight=26)

        # Строка статуса
        self.status_var = tk.StringVar(value="Добро пожаловать!")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x")

        # Сборка backend-зависимостей
        self.build_services()

        # Контейнер для экранов
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Создание экранов
        self.frames = {}
        self.frames["catalog"] = CatalogFrame(self.container, self.catalog_service, self.cart_service)
        self.frames["catalog"].grid(row=0, column=0, sticky="nsew")

        self.frames["cart"] = CartFrame(self.container, self.cart_service, self.catalog_service,
                                        on_checkout=self.show_checkout)
        self.frames["cart"].grid(row=0, column=0, sticky="nsew")

        self.frames["checkout"] = CheckoutFrame(self.container, self.cart_service, self.order_service,
                                                self.discount_service,
                                                on_back_to_catalog=self.show_catalog)
        self.frames["checkout"].grid(row=0, column=0, sticky="nsew")

        # Панель навигации
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(side="top", fill="x", padx=10, pady=5)
        ttk.Button(nav_frame, text="Каталог", command=self.show_catalog).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Корзина", command=self.show_cart).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Оформить заказ", command=self.show_checkout).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Выход", command=self.root.quit).pack(side="right", padx=5)

        # Показываем каталог
        self.show_catalog()

    def build_services(self):
        if BACKEND_AVAILABLE:
            # Реальные сервисы
            self.connection = get_connection()
            self.cat_repo = CategoryRepository(self.connection)
            self.prod_repo = ProductRepository(self.connection)
            self.size_repo = SizesRepository(self.connection)
            self.cust_repo = ByerRepository(self.connection) if ByerRepository else None
            self.order_repo = OrderRepository(self.connection) if 'OrderRepository' in globals() else None
            self.promo_repo = PromoCodeRepository(self.connection) if PromoCodeRepository else None

            self.catalog_service = CatalogService(self.prod_repo, self.cat_repo, self.size_repo)
            self.cart_service = CartService(self.prod_repo, self.size_repo)
            self.discount_service = DiscountService(self.promo_repo) if self.promo_repo else None
            if self.discount_service is None:
                self.discount_service = FakeDiscountService()
            self.order_service = OrderServiceWithDiscount(self.order_repo, self.prod_repo, self.size_repo,
                                                          self.cust_repo, self.discount_service) if self.order_repo else None
            if self.order_service is None:
                self.order_service = FakeOrderService()
        else:
            # Заглушки
            self.connection = None
            self.cat_repo = CategoryRepository()
            self.prod_repo = ProductRepository()
            self.size_repo = SizesRepository()
            # Для демонстрации добавим тестовые остатки
            if hasattr(self.size_repo, 'add_stock'):
                for p in self.prod_repo.get_all():
                    for s in getattr(p, 'sizes', ["ONE"]):
                        self.size_repo.add_stock(p.id, s, 10)

            self.catalog_service = CatalogService(self.prod_repo, self.cat_repo, self.size_repo)
            self.cart_service = CartService()
            self.discount_service = DiscountService()
            self.order_service = OrderService()

    def show_frame(self, name):
        for f in self.frames.values():
            f.grid_remove()
        frame = self.frames[name]
        frame.grid()
        if hasattr(frame, "refresh"):
            frame.refresh()
        self.status_var.set(f"Экран: {name.capitalize()}")

    def show_catalog(self):
        self.show_frame("catalog")

    def show_cart(self):
        self.show_frame("cart")

    def show_checkout(self):
        self.show_frame("checkout")

    def run(self):
        self.root.mainloop()
        if self.connection:
            self.connection.close()


# Задание 6
# Добавьте общую обработку ошибок и сообщений.
# Пользователь не должен видеть traceback при обычных ошибках ввода.

# TODO: добавить обработку ошибок


# Задание 7
# Проверьте полный пользовательский сценарий:
# каталог -> выбор товара -> корзина -> изменение количества -> оформление заказа.


# TODO: проверить полный сценарий

if __name__ == "__main__":
    app = ClothingStoreDesktopApp()
    app.run()

# Задание 8
# Улучшите внешний вид:
# отступы, ширина колонок, названия кнопок, начальный размер окна,
# запрет слишком маленького размера окна.


# TODO: улучшить удобство интерфейса
