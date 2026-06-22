"""
Этап 07. Оформление заказа

Цель: создать экран оформления заказа с формой покупателя, проверкой данных,
промокодом и созданием заказа через backend-сервис.
"""


# Задание 1
# Создайте CheckoutFrame.
# Он должен получать корзину, сервис заказов и сервис скидок через __init__.


# TODO: создать экран оформления заказа


import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# Вспомогательные заглушки (для автономной работы)
# ============================================================

class FakeCartService:
    def __init__(self):
        self.items = []
        self._promo_code = None

    def add_to_cart(self, product_id, name, size, quantity, price):
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
        self._promo_code = None

    def get_items(self):
        return self.items

    def get_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def is_empty(self):
        return len(self.items) == 0

    def find_item(self, product_id, size):
        for item in self.items:
            if item["product_id"] == product_id and item["size"] == size:
                return item
        return None

    def set_promo_code(self, code):
        self._promo_code = code

    def get_promo_code(self):
        return self._promo_code

    def check_stock(self, product_id, size, quantity):
        return True

class FakeDiscountService:
    def apply_promo(self, total, code):
        if code == "SALE10":
            discount = int(total * 0.1)
            return total - discount, discount
        elif code == "SALE20":
            discount = int(total * 0.2)
            return total - discount, discount
        elif code == "WELCOME":
            discount = int(total * 0.15)
            return total - discount, discount
        else:
            raise ValueError("Промокод не найден или недействителен")

class FakeOrderService:
    def __init__(self):
        self.order_counter = 0

    def create_order(self, cart_service, customer_data, promo_code=None):
        if cart_service.is_empty():
            raise ValueError("Корзина пуста")
        if not customer_data.get("name", "").strip():
            raise ValueError("Имя обязательно")
        if not customer_data.get("contact", "").strip():
            raise ValueError("Контакт (телефон или email) обязателен")
        if not customer_data.get("city", "").strip():
            raise ValueError("Город обязателен")
        if not customer_data.get("street", "").strip():
            raise ValueError("Улица обязательна")
        if not customer_data.get("house", "").strip():
            raise ValueError("Дом обязателен")
        if promo_code == "ERROR_STOCK":
            raise ValueError("Недостаточно товара на складе")
        self.order_counter += 1
        return {"id": self.order_counter, "total": cart_service.get_total()}

# ============================================================
# ЗАДАНИЕ 1: Создайте CheckoutFrame.
# Он должен получать корзину, сервис заказов и сервис скидок через __init__.
# ============================================================

class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, cart_service, order_service, discount_service,
                 on_order_success=None, on_back_to_catalog=None):
        super().__init__(parent)
        self.cart_service = cart_service
        self.order_service = order_service
        self.discount_service = discount_service
        self.on_order_success = on_order_success
        self.on_back_to_catalog = on_back_to_catalog

        # Переменные для формы
        self.name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.street_var = tk.StringVar()
        self.house_var = tk.StringVar()
        self.apartment_var = tk.StringVar(value="")
        self.promo_var = tk.StringVar()

        # Переменные для отображения итогов
        self.subtotal_var = tk.StringVar(value="0 руб.")
        self.discount_var = tk.StringVar(value="0 руб.")
        self.total_var = tk.StringVar(value="0 руб.")
        self.promo_status_var = tk.StringVar(value="Промокод не применён")

        self._build_ui()
        self.refresh()

# Задание 2
# Добавьте форму покупателя:
# имя, телефон или email, город, улица, дом, квартира.


# TODO: добавить форму покупателя и адреса


    def _build_ui(self):
        # Основная структура с двумя колонками
        main_paned = ttk.PanedWindow(self, orient="horizontal")
        main_paned.pack(fill="both", expand=True, padx=10, pady=5)

        # Левая панель: форма
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        ttk.Label(left_frame, text="Данные для доставки", font=("Arial", 12)).pack(anchor="w", pady=5)

        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill="x", padx=5, pady=5)

        row = 0
        ttk.Label(form_frame, text="Имя*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1

        ttk.Label(form_frame, text="Телефон или email*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        self.contact_entry = ttk.Entry(form_frame, textvariable=self.contact_var, width=30)
        self.contact_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1

        ttk.Label(form_frame, text="Город*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        self.city_entry = ttk.Entry(form_frame, textvariable=self.city_var, width=30)
        self.city_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1

        ttk.Label(form_frame, text="Улица*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        self.street_entry = ttk.Entry(form_frame, textvariable=self.street_var, width=30)
        self.street_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1

        ttk.Label(form_frame, text="Дом*").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        self.house_entry = ttk.Entry(form_frame, textvariable=self.house_var, width=30)
        self.house_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        row += 1

        ttk.Label(form_frame, text="Квартира").grid(row=row, column=0, sticky="w", padx=5, pady=3)
        self.apartment_entry = ttk.Entry(form_frame, textvariable=self.apartment_var, width=30)
        self.apartment_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        form_frame.columnconfigure(1, weight=1)


# Задание 3
# Добавьте поле промокода и кнопку "Применить".
# Результат применения скидки показывайте в интерфейсе.


# TODO: добавить промокод


        promo_frame = ttk.Frame(left_frame)
        promo_frame.pack(fill="x", padx=5, pady=10)
        ttk.Label(promo_frame, text="Промокод:").pack(side="left", padx=5)
        self.promo_entry = ttk.Entry(promo_frame, textvariable=self.promo_var, width=20)
        self.promo_entry.pack(side="left", padx=5)
        ttk.Button(promo_frame, text="Применить", command=self.apply_promo).pack(side="left", padx=5)
        ttk.Label(left_frame, textvariable=self.promo_status_var, foreground="blue").pack(anchor="w", padx=10, pady=2)

        # Правая панель: сводка заказа
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)

# Задание 4
# Добавьте блок с кратким составом заказа и итоговой суммой.
# Он должен обновляться при переходе на экран оформления.


# TODO: добавить сводку заказа

        ttk.Label(right_frame, text="Состав заказа", font=("Arial", 12)).pack(anchor="w", pady=5)

        self.summary_tree = ttk.Treeview(right_frame, columns=("name", "size", "quantity", "price"),
                                         show="headings", height=8)
        self.summary_tree.heading("name", text="Товар")
        self.summary_tree.heading("size", text="Размер")
        self.summary_tree.heading("quantity", text="Кол-во")
        self.summary_tree.heading("price", text="Сумма")
        self.summary_tree.column("name", width=150)
        self.summary_tree.column("size", width=60)
        self.summary_tree.column("quantity", width=60, anchor="center")
        self.summary_tree.column("price", width=80, anchor="e")

        scroll = ttk.Scrollbar(right_frame, orient="vertical", command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scroll.set)
        self.summary_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scroll.pack(side="right", fill="y", pady=5)

        # Блок итогов
        total_frame = ttk.Frame(right_frame)
        total_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(total_frame, text="Сумма без скидки:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(total_frame, textvariable=self.subtotal_var).grid(row=0, column=1, sticky="e", padx=5)

        ttk.Label(total_frame, text="Скидка:").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(total_frame, textvariable=self.discount_var, foreground="green").grid(row=1, column=1, sticky="e", padx=5)

        ttk.Label(total_frame, text="Итого к оплате:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(total_frame, textvariable=self.total_var, font=("Arial", 12, "bold")).grid(row=2, column=1, sticky="e", padx=5)
        total_frame.columnconfigure(0, weight=1)
        total_frame.columnconfigure(1, weight=1)

# Задание 5
# Добавьте простую проверку формы на уровне GUI.
# Например, имя и контакт не должны быть пустыми.


# TODO: добавить проверку полей формы


# Задание 6
# Добавьте кнопку "Оформить заказ".
# Она должна вызвать backend-сервис оформления заказа.


# TODO: добавить создание заказа


        ttk.Button(right_frame, text="Оформить заказ", command=self.place_order).pack(pady=10)

        # Строка статуса
        self.status_var = tk.StringVar(value="Заполните данные для оформления")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)




    def refresh(self):
        """Обновляет сводку заказа и итоговые суммы."""
        for row in self.summary_tree.get_children():
            self.summary_tree.delete(row)

        items = self.cart_service.get_items()
        if not items:
            self.status_var.set("Корзина пуста. Добавьте товары.")
            self.subtotal_var.set("0 руб.")
            self.discount_var.set("0 руб.")
            self.total_var.set("0 руб.")
            return

        subtotal = 0
        for item in items:
            total_item = item["price"] * item["quantity"]
            subtotal += total_item
            self.summary_tree.insert("", "end", values=(item["name"], item["size"], item["quantity"], total_item))

        promo_code = self.cart_service.get_promo_code()
        if promo_code:
            try:
                final, discount = self.discount_service.apply_promo(subtotal, promo_code)
                self.subtotal_var.set(f"{subtotal} руб.")
                self.discount_var.set(f"-{discount} руб.")
                self.total_var.set(f"{final} руб.")
                self.promo_status_var.set(f"Промокод {promo_code} применён, скидка {discount} руб.")
                self.status_var.set(f"Промокод активен, итог: {final} руб.")
            except Exception as e:
                self.cart_service.set_promo_code(None)
                self.promo_var.set("")
                self.promo_status_var.set("Ошибка промокода: " + str(e))
                self.subtotal_var.set(f"{subtotal} руб.")
                self.discount_var.set("0 руб.")
                self.total_var.set(f"{subtotal} руб.")
                self.status_var.set("Промокод отменён")
        else:
            self.subtotal_var.set(f"{subtotal} руб.")
            self.discount_var.set("0 руб.")
            self.total_var.set(f"{subtotal} руб.")
            self.promo_status_var.set("Промокод не применён")
            self.status_var.set(f"Итоговая сумма: {subtotal} руб.")

    # ============================================================
    # Обработчик применения промокода (задание 3)
    # ============================================================

    def apply_promo(self):
        code = self.promo_var.get().strip()
        if not code:
            messagebox.showerror("Ошибка", "Введите код промокода")
            return
        try:
            subtotal = self.cart_service.get_total()
            final, discount = self.discount_service.apply_promo(subtotal, code)
            self.cart_service.set_promo_code(code)
            self.refresh()
            messagebox.showinfo("Успешно", f"Промокод применён. Скидка {discount} руб.")
        except Exception as e:
            self.cart_service.set_promo_code(None)
            self.promo_status_var.set("Ошибка: " + str(e))
            self.refresh()
            messagebox.showerror("Ошибка", str(e))

    # ============================================================
    # ЗАДАНИЕ 5: Добавьте простую проверку формы на уровне GUI.
    # Например, имя и контакт не должны быть пустыми.
    # ============================================================

    def validate_form(self):
        errors = []
        if not self.name_var.get().strip():
            errors.append("Имя")
        if not self.contact_var.get().strip():
            errors.append("Телефон или email")
        if not self.city_var.get().strip():
            errors.append("Город")
        if not self.street_var.get().strip():
            errors.append("Улица")
        if not self.house_var.get().strip():
            errors.append("Дом")
        if errors:
            messagebox.showerror("Ошибка", f"Заполните обязательные поля: {', '.join(errors)}")
            return False
        return True

    # ============================================================
    # ЗАДАНИЕ 6: Кнопка "Оформить заказ" (реализована в _build_ui)
    # и метод place_order, который вызывает backend-сервис.
    # ============================================================

    def place_order(self):
        if self.cart_service.is_empty():
            messagebox.showerror("Ошибка", "Корзина пуста. Добавьте товары.")
            return

        if not self.validate_form():
            return

        customer_data = {
            "name": self.name_var.get().strip(),
            "contact": self.contact_var.get().strip(),
            "city": self.city_var.get().strip(),
            "street": self.street_var.get().strip(),
            "house": self.house_var.get().strip(),
            "apartment": self.apartment_var.get().strip(),
        }

        promo_code = self.cart_service.get_promo_code()

        try:
            order = self.order_service.create_order(self.cart_service, customer_data, promo_code)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            self.refresh()
            return
        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", str(e))
            self.refresh()
            return
        
# Задание 7
# После успешного оформления покажите номер заказа,
# очистите корзину и верните пользователя в каталог или на экран подтверждения.


# TODO: добавить успешное завершение заказа


        self.cart_service.clear()
        self.cart_service.set_promo_code(None)
        self.promo_var.set("")
        self.promo_status_var.set("Промокод не применён")
        self.refresh()

        messagebox.showinfo("Заказ оформлен", f"Ваш заказ №{order['id']} оформлен на сумму {order['total']} руб.\nСпасибо за покупку!")

        if self.on_back_to_catalog:
            self.on_back_to_catalog()
        else:
            self.status_var.set(f"Заказ №{order['id']} оформлен, сумма {order['total']} руб.")


# Задание 8
# Проверьте ошибки:
# пустая корзина, пустые поля, неверный промокод, нехватка товара.


# TODO: проверить оформление заказа


if __name__ == "__main__":
    # Создаём заглушки
    cart = FakeCartService()
    discount = FakeDiscountService()
    order = FakeOrderService()

    # Наполняем корзину тестовыми товарами
    cart.add_to_cart(1, "Кроссовки", "42", 2, 2500)
    cart.add_to_cart(2, "Платье", "M", 1, 3500)

    # Создаём окно и экран оформления
    root = tk.Tk()
    root.title("Магазин одежды - Оформление заказа")
    root.geometry("1000x600")

    # Колбэки для возврата в каталог (заглушки)
    def go_to_catalog():
        messagebox.showinfo("Возврат", "Возврат в каталог (заглушка)")

    # Создаём экран
    frame = CheckoutFrame(root, cart, order, discount,
                          on_back_to_catalog=go_to_catalog)
    frame.pack(fill="both", expand=True)

    root.mainloop()