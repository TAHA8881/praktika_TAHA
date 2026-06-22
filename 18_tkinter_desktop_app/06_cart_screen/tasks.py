"""
Этап 06. Экран корзины

Цель: создать экран корзины, который показывает выбранные товары,
позволяет менять количество и пересчитывает итоговую сумму.
"""


# Задание 1
# Создайте CartFrame.
# Он должен получать объект корзины или сервис корзины через __init__.


# TODO: создать экран корзины


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ============================================================
# Вспомогательные заглушки (заменятся на реальные сервисы)
# ============================================================

class FakeCartService:
    """Заглушка сервиса корзины с хранением позиций в памяти."""
    def __init__(self):
        self.items = []  # каждый элемент: dict с полями product_id, name, size, quantity, price

    def add_to_cart(self, product_id, name, size, quantity, price):
        # Проверяем, есть ли уже такая позиция
        for item in self.items:
            if item["product_id"] == product_id and item["size"] == size:
                item["quantity"] += quantity
                return
        self.items.append({
            "product_id": product_id,
            "name": name,
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
                    self.remove_item(product_id, size)
                else:
                    item["quantity"] = new_quantity
                return

    def clear(self):
        self.items.clear()

    def get_items(self):
        return self.items

    def get_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def is_empty(self):
        return len(self.items) == 0

    # Вспомогательный метод для поиска позиции по id и размеру (для проверок)
    def find_item(self, product_id, size):
        for item in self.items:
            if item["product_id"] == product_id and item["size"] == size:
                return item
        return None

    # Заглушка проверки остатка – всегда доступно
    def check_stock(self, product_id, size, quantity):
        return True


class FakeCatalogService:
    """Заглушка каталога для получения названий товаров."""
    def __init__(self):
        self.products = {
            1: {"name": "Кроссовки", "price": 2500},
            2: {"name": "Платье", "price": 3500},
            3: {"name": "Ботинки", "price": 4500},
            4: {"name": "Сумка", "price": 1200},
            5: {"name": "Ремень", "price": 800},
            6: {"name": "Куртка", "price": 5500},
        }

    def get_product_name(self, product_id):
        return self.products.get(product_id, {}).get("name", "Неизвестный товар")

    def get_product_price(self, product_id):
        return self.products.get(product_id, {}).get("price", 0)


# ============================================================
# Основной класс экрана корзины
# ============================================================

class CartFrame(ttk.Frame):
    """Экран корзины."""
    # Задание 1: получает сервис корзины и (опционально) сервис каталога и callback перехода
    def __init__(self, parent, cart_service, catalog_service=None, on_checkout=None):
        super().__init__(parent)
        self.cart_service = cart_service
        self.catalog_service = catalog_service or FakeCatalogService()
        self.on_checkout = on_checkout  # функция для переключения на экран оформления

        # Переменная для хранения выбранной позиции
        self.selected_item = None  # будет хранить (product_id, size)
        self.row_to_item = {}      # связь идентификатора строки с (product_id, size)

        # Построение интерфейса
        self._build_ui()

        # Первоначальное обновление
        self.refresh_cart()

    def _build_ui(self):
        # Заголовок
        ttk.Label(self, text="Корзина", font=("Arial", 16)).pack(pady=10)

# Задание 2
# Добавьте Treeview для позиций корзины.
# Колонки: товар, размер, цена, количество, сумма.


# TODO: добавить таблицу корзины

        columns = ("product_id", "name", "size", "price", "quantity", "total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("product_id", text="ID")
        self.tree.heading("name", text="Товар")
        self.tree.heading("size", text="Размер")
        self.tree.heading("price", text="Цена, руб.")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("total", text="Сумма, руб.")

        self.tree.column("product_id", width=50, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("size", width=60, anchor="center")
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("total", width=100, anchor="e")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scroll.pack(side="right", fill="y", pady=5)

# Задание 3
# Добавьте метод refresh_cart().
# Он должен обновлять таблицу и итоговую сумму.


# TODO: добавить обновление корзины


# Задание 4
# Добавьте выбор позиции корзины.
# Сохраняйте выбранную позицию для дальнейших действий.


# TODO: добавить выбор позиции корзины

        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Панель итогов
        self.total_frame = ttk.Frame(self)
        self.total_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.total_frame, text="Итоговая сумма:", font=("Arial", 12)).pack(side="left", padx=5)
        self.total_var = tk.StringVar(value="0 руб.")
        ttk.Label(self.total_frame, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(side="left", padx=5)

        # Панель действий
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=10)


# Задание 5
# Добавьте изменение количества выбранной позиции.
# Обработайте неверное количество и нехватку товара.


# TODO: добавить изменение количества

        self.change_qty_btn = ttk.Button(action_frame, text="Изменить количество", command=self.change_quantity)
        self.change_qty_btn.pack(side="left", padx=5)


# Задание 6
# Добавьте удаление выбранной позиции.
# Если позиция не выбрана, покажите ошибку.


# TODO: добавить удаление позиции

        self.remove_btn = ttk.Button(action_frame, text="Удалить позицию", command=self.remove_selected)
        self.remove_btn.pack(side="left", padx=5)


# Задание 7
# Добавьте очистку всей корзины с подтверждением через messagebox.askyesno().


# TODO: добавить очистку корзины

        self.clear_btn = ttk.Button(action_frame, text="Очистить корзину", command=self.clear_cart)
        self.clear_btn.pack(side="left", padx=5)


# Задание 8
# Добавьте кнопку перехода к оформлению заказа.
# Если корзина пуста, оформление начинаться не должно.


# TODO: добавить переход к оформлению заказа

        self.checkout_btn = ttk.Button(action_frame, text="Перейти к оформлению", command=self.go_to_checkout)
        self.checkout_btn.pack(side="right", padx=5)

        # Строка статуса
        self.status_var = tk.StringVar(value="Готово")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)


    # ============================================================
    # Задание 3: обновление корзины
    # ============================================================

    def refresh_cart(self):
        """Обновляет таблицу и итоговую сумму."""
        # Очищаем таблицу и словарь
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)
        self.row_to_item.clear()

        items = self.cart_service.get_items()
        total = self.cart_service.get_total()

        for item in items:
            product_id = item["product_id"]
            name = item["name"]
            size = item["size"]
            price = item["price"]
            quantity = item["quantity"]
            item_total = price * quantity
            row_id = self.tree.insert("", "end", values=(product_id, name, size, price, quantity, item_total))
            self.row_to_item[row_id] = (product_id, size)

        self.total_var.set(f"{total} руб.")
        self.status_var.set(f"В корзине {len(items)} позиций. Итого: {total} руб.")

        # Сбрасываем выбор
        self.selected_item = None

    # ============================================================
    # Задание 4: выбор позиции корзины
    # ============================================================

    def on_item_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            self.selected_item = None
            return
        row_id = selected[0]
        self.selected_item = self.row_to_item.get(row_id)
        if self.selected_item:
            product_id, size = self.selected_item
            # Найдём название для статуса
            name = self.catalog_service.get_product_name(product_id)
            self.status_var.set(f"Выбрана позиция: {name} (размер {size})")

    # ============================================================
    # Задание 5: изменение количества выбранной позиции
    # ============================================================

    def change_quantity(self):
        if not self.selected_item:
            messagebox.showerror("Ошибка", "Не выбрана позиция для изменения.")
            return

        product_id, size = self.selected_item
        item = self.cart_service.find_item(product_id, size)
        if not item:
            messagebox.showerror("Ошибка", "Позиция не найдена в корзине.")
            self.refresh_cart()
            return

        # Запрашиваем новое количество
        new_qty_str = simpledialog.askstring(
            "Изменить количество",
            f"Товар: {item['name']} (размер {size})\nВведите новое количество (0 для удаления):",
            initialvalue=str(item["quantity"])
        )
        if new_qty_str is None:
            return  # отмена

        try:
            new_qty = int(new_qty_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом.")
            return

        if new_qty < 0:
            messagebox.showerror("Ошибка", "Количество не может быть отрицательным.")
            return

        # Проверка остатка (заглушка – всегда true)
        if new_qty > 0 and not self.cart_service.check_stock(product_id, size, new_qty):
            messagebox.showerror("Ошибка", "Недостаточно товара на складе.")
            return

        # Обновляем количество через сервис
        self.cart_service.update_quantity(product_id, size, new_qty)
        self.refresh_cart()
        self.status_var.set(f"Количество изменено для товара {item['name']} (размер {size})")

    # ============================================================
    # Задание 6: удаление выбранной позиции
    # ============================================================

    def remove_selected(self):
        if not self.selected_item:
            messagebox.showerror("Ошибка", "Не выбрана позиция для удаления.")
            return

        product_id, size = self.selected_item
        item = self.cart_service.find_item(product_id, size)
        if not item:
            messagebox.showerror("Ошибка", "Позиция не найдена.")
            self.refresh_cart()
            return

        # Подтверждение
        if messagebox.askyesno("Подтверждение", f"Удалить товар '{item['name']}' (размер {size})?"):
            self.cart_service.remove_item(product_id, size)
            self.refresh_cart()
            self.status_var.set(f"Позиция '{item['name']}' удалена.")

    # ============================================================
    # Задание 7: очистка корзины с подтверждением
    # ============================================================

    def clear_cart(self):
        if self.cart_service.is_empty():
            messagebox.showinfo("Информация", "Корзина уже пуста.")
            return

        if messagebox.askyesno("Подтверждение", "Очистить всю корзину?"):
            self.cart_service.clear()
            self.refresh_cart()
            self.status_var.set("Корзина очищена.")

    # ============================================================
    # Задание 8: переход к оформлению заказа
    # ============================================================

    def go_to_checkout(self):
        if self.cart_service.is_empty():
            messagebox.showerror("Ошибка", "Корзина пуста. Добавьте товары перед оформлением.")
            return

        if self.on_checkout:
            self.on_checkout()
        else:
            messagebox.showinfo("Информация", "Переход к оформлению заказа (заглушка).")

# ============================================================
# Проверка работоспособности экрана корзины
# ============================================================

if __name__ == "__main__":
    # Создаём заглушки сервисов
    cart = FakeCartService()
    catalog = FakeCatalogService()

    # Заполняем корзину тестовыми данными
    cart.add_to_cart(1, "Кроссовки", "42", 2, 2500)
    cart.add_to_cart(2, "Платье", "M", 1, 3500)
    cart.add_to_cart(3, "Ботинки", "43", 1, 4500)

    # Создаём окно
    root = tk.Tk()
    root.title("Магазин одежды - Корзина")
    root.geometry("800x500")

    # Функция-заглушка для перехода к оформлению
    def on_checkout():
        messagebox.showinfo("Переход", "Переход к экрану оформления заказа (заглушка).")

    # Создаём экран корзины
    frame = CartFrame(root, cart, catalog, on_checkout=on_checkout)
    frame.pack(fill="both", expand=True)

    root.mainloop()