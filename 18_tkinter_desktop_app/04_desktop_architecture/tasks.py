"""
Этап 04. Архитектура desktop-приложения

Цель: отделить GUI-код от backend-логики и подготовить основу приложения,
которое сможет использовать код из задания 17.
"""


# Задание 1
# Создайте класс DesktopApp.
# Он должен создавать главное окно и хранить ссылки на сервисы приложения.


# TODO: создать класс DesktopApp

import tkinter as tk
from tkinter import ttk, messagebox

class DesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Магазин одежды")
        self.root.geometry("850x600")
        
        # Строка статуса (будет позже)
        self.status_var = tk.StringVar(value="Готово")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x")
        
        # Контейнер для экранов
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Здесь позже будут созданы экраны и сервисы
        self.frames = {}
        self.catalog_service = None
        self.cart_service = None
        self.discount_service = None
        self.order_service = None
        
        # Меню
        self._build_menu()
    
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Меню", menu=view_menu)
        view_menu.add_command(label="Каталог", command=lambda: self.show_frame("catalog"))
        view_menu.add_command(label="Корзина", command=lambda: self.show_frame("cart"))
        view_menu.add_command(label="Оформить заказ", command=lambda: self.show_frame("checkout"))
        view_menu.add_separator()
        view_menu.add_command(label="Выход", command=self.root.quit)
    
    def show_frame(self, name):
        # Задание 3: переключение экранов (будет реализовано позже)
        pass
    
    def show_error(self, message):
        # Задание 6: обработка ошибок (будет реализовано позже)
        pass
    
    def run(self):
        self.root.mainloop()

# Задание 2
# Создайте отдельные классы экранов:
# CatalogFrame, CartFrame, CheckoutFrame.
# Пока каждый экран может показывать только заголовок и пару кнопок.


# TODO: создать классы экранов


class CatalogFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_ui()
    
    def _build_ui(self):
        ttk.Label(self, text="Каталог товаров", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self, text="Здесь будет таблица товаров").pack(pady=20)
        ttk.Button(self, text="Заглушка: добавить в корзину").pack(pady=5)
    
    def refresh(self):
        pass

class CartFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_ui()
    
    def _build_ui(self):
        ttk.Label(self, text="Корзина", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self, text="Здесь будут товары в корзине").pack(pady=20)
    
    def refresh(self):
        pass

class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build_ui()
    
    def _build_ui(self):
        ttk.Label(self, text="Оформление заказа", font=("Arial", 14)).pack(pady=10)
        ttk.Label(self, text="Здесь будет форма заказа").pack(pady=20)
    
    def refresh(self):
        pass


# Задание 3
# Добавьте переключение экранов.
# Например, метод show_frame(name), который скрывает текущий экран
# и показывает выбранный.


# TODO: добавить переключение между экранами

# Расширяем класс DesktopApp (можно переопределить или дописать)
# В реальном коде мы бы переписали класс, но для наглядности показываем изменение

def show_frame_implementation(self, name):
    for frame in self.frames.values():
        frame.pack_forget()
    frame = self.frames[name]
    frame.pack(fill="both", expand=True)
    if hasattr(frame, "refresh"):
        frame.refresh()
    self.status_var.set(f"Экран: {name}")

# Применяем патч (в реальном проекте просто переопределяем метод в классе)
DesktopApp.show_frame = show_frame_implementation


# Задание 4
# Подготовьте функцию или класс, который собирает backend-зависимости:
# репозитории, сервис каталога, корзину, сервис заказов.
# Если backend из задания 17 еще не готов, используйте временные заглушки.


# TODO: подготовить сборку зависимостей


class FakeProduct:
    def __init__(self, id, name, category_id, price, color, description, is_active):
        self.id = id
        self.product_name = name
        self.category_id = category_id
        self.price = price
        self.color = color
        self.description = description
        self.is_active = is_active

class FakeCatalogService:
    def __init__(self):
        self.products = [
            FakeProduct(1, "Кроссовки", 1, 2500, "белый", "", True),
            FakeProduct(2, "Платье", 2, 3500, "красный", "", True),
            FakeProduct(3, "Ботинки", 1, 4500, "черный", "", True),
        ]
        self.categories = [{"id": 1, "name": "Обувь"}, {"id": 2, "name": "Одежда"}]
    
    def get_active_products(self):
        return [p for p in self.products if p.is_active]
    
    def search_products(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.get_active_products() if keyword in p.product_name.lower()]

class FakeCartService:
    def __init__(self):
        self.items = []
    
    def add_to_cart(self, product_id, size, quantity):
        self.items.append({"product_id": product_id, "size": size, "quantity": quantity})
    
    def get_cart_items(self):
        return self.items
    
    def clear_cart(self):
        self.items.clear()
    
    def is_empty(self):
        return len(self.items) == 0

class FakeOrderService:
    def create_order(self, cart_service, customer_id, promocode=None):
        if cart_service.is_empty():
            raise ValueError("Корзина пуста")
        return {"id": 123, "total": 1000}

class FakeDiscountService:
    def apply_promo(self, total, code):
        if code == "SALE10":
            return total * 0.9, total * 0.1
        raise ValueError("Промокод не найден")

# Задание 5
# Запретите прямую работу с SQL внутри классов интерфейса.
# Все данные должны приходить через сервисы или временные заглушки.


# TODO: проверить границы ответственности


# Задание 6
# Добавьте единое место для обработки ошибок сервисов.
# Например, вспомогательный метод show_error(error).


# TODO: добавить общий показ ошибок

def show_error_implementation(self, message):
    self.status_var.set(f"Ошибка: {message}")
    messagebox.showerror("Ошибка", message)

DesktopApp.show_error = show_error_implementation


# Задание 7
# Проверьте, что приложение открывается и можно переключаться
# между каталогом, корзиной и оформлением заказа.


# TODO: проверить навигацию приложения

if __name__ == "__main__":
    # Создаём приложение
    app = DesktopApp()
    
    # Задание 4: подключаем заглушки
    app.catalog_service = FakeCatalogService()
    app.cart_service = FakeCartService()
    app.discount_service = FakeDiscountService()
    app.order_service = FakeOrderService()
    
    # Задание 2: создаём экраны (теперь сервисы уже есть)
    app.frames = {
        "catalog": CatalogFrame(app.container, app),
        "cart": CartFrame(app.container, app),
        "checkout": CheckoutFrame(app.container, app),
    }
    for frame in app.frames.values():
        frame.pack(fill="both", expand=True)
        frame.pack_forget()
    
    # Задание 3: показываем начальный экран
    app.show_frame("catalog")
    
    # Запускаем
    app.run()