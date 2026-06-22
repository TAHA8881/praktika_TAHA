"""
Этап 08. Итоговое консольное приложение

Цель: собрать модели, репозитории, сервисы, корзину, скидки, заказы
и PostgreSQL-хранилище в одну консольную программу.

Консольный интерфейс и сборку приложения создавайте прямо в этом файле.
Модели, репозитории и сервисы импортируйте из предыдущих этапов.
"""


# Задание 1
# Подготовьте структуру итогового приложения.
# Разделите код так, чтобы запуск был в одном месте, а классы жили по слоям.


# TODO: подготовить структуру итогового приложения

import sys
from importlib import import_module
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# --- Модели из этапа 01 ---
domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes
Byer = domain.Byer

# --- Репозитории из этапа 03 ---
repos = import_module("17_clothing_store_project.03_repositories.tasks")
CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
SizesRepository = repos.SizesRepository
ByerRepository = repos.ByerRepository
get_connection = repos.get_connection

# --- Сервисы этапа 04 (каталог) ---
catalog_mod = import_module("17_clothing_store_project.04_catalog_service.tasks")
CatalogService = catalog_mod.CatalogService

# --- Сервисы этапа 05 (корзина) ---
cart_mod = import_module("17_clothing_store_project.05_cart.tasks")
CartService = cart_mod.CartService
Cart = cart_mod.Cart

# --- Сервисы этапа 06 (заказы) ---
order_mod = import_module("17_clothing_store_project.06_orders.tasks")
OrderRepository = order_mod.OrderRepository
OrderService = order_mod.OrderService

# --- Сервисы этапа 07 (промокоды, адреса, скидки) ---
promo_mod = import_module("17_clothing_store_project.07_promocodes.tasks")
Address = promo_mod.Address
AddressRepository = promo_mod.AddressRepository
PromoCode = promo_mod.PromoCode
PromoCodeRepository = promo_mod.PromoCodeRepository
DiscountService = promo_mod.DiscountService
OrderServiceWithDiscount = promo_mod.OrderServiceWithDiscount


# Задание 2
# Создайте стартовые данные.
# В базе должно быть несколько категорий, товаров, остатков по размерам,
# покупателей, адресов и промокодов.
# Повторный запуск программы не должен бесконечно дублировать стартовые данные.


# TODO: добавить стартовые данные

def init_data(conn):
    """Создаёт начальные данные, если их нет."""
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    size_repo = SizesRepository(conn)
    cust_repo = ByerRepository(conn)
    promo_repo = PromoCodeRepository(conn)
    addr_repo = AddressRepository(conn)

    # Категории
    categories = [
        Category(1, "Обувь", "Женская и мужская обувь"),
        Category(2, "Одежда", "Верхняя одежда, платья, костюмы"),
        Category(3, "Аксессуары", "Сумки, ремни, головные уборы")
    ]
    for cat in categories:
        if cat_repo.get_by_id_c(cat.category_id) is None:
            cat_repo.add_categories(cat)

    # Товары
    products = [
        Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные кроссовки", True),
        Product(2, "Платье", 2, 3500, "красный", "Вечернее платье", True),
        Product(3, "Ботинки", 1, 4500, "черный", "Кожаные ботинки", True),
        Product(4, "Сумка", 3, 1200, "коричневый", "Кожаная сумка", True),
        Product(5, "Ремень", 3, 800, "черный", "Кожаный ремень", False)  # неактивный
    ]
    for prod in products:
        if prod_repo.get_by_id_p(prod.id) is None:
            prod_repo.add_product(prod)

    # Остатки по размерам
    sizes = [
        LeftSizes(1, 1, "42", 10),
        LeftSizes(2, 1, "43", 5),
        LeftSizes(3, 2, "M", 7),
        LeftSizes(4, 2, "L", 3),
        LeftSizes(5, 3, "41", 4),
        LeftSizes(6, 4, "ONE", 8)
    ]
    for s in sizes:
        if size_repo.get_by_id_ls(s.store_id) is None:
            size_repo.add_left_sizes(s)

    # Покупатель (тестовый)
    customers = [
        Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789"),
        Byer(2, "Мария Смирнова", "maria@mail.ru", "+79234567890")
    ]
    for cust in customers:
        if cust_repo.get_by_id_b(cust.byer_id) is None:
            cust_repo.add_byer(cust)

    # Адреса
    addresses = [
        Address(1, 1, "ул. Ленина, д.1, кв.5", True),
        Address(2, 2, "пр. Мира, д.10, кв.20", True)
    ]
    for addr in addresses:
        if addr_repo.get_by_id(addr.id) is None:
            addr_repo.add(addr)

    # Промокоды
    promos = [
        PromoCode("SALE10", 10, 1000, True),
        PromoCode("SALE20", 20, 2000, True),
        PromoCode("WELCOME", 15, 500, True),
        PromoCode("EXPIRED", 5, 100, False)
    ]
    for p in promos:
        if promo_repo.get_by_code(p.code) is None:
            promo_repo.add(p)


# Задание 3
# Соберите репозитории и сервисы.
# Создайте подключение к PostgreSQL один раз и передайте его в репозитории.
# Проверьте, что интерфейс обращается к сервисам, а не к таблицам напрямую.


# TODO: собрать зависимости приложения

class ConsoleApp:
    """Главный класс консольного интерфейса."""

    def __init__(self, conn):
        self.conn = conn

        # Инициализируем репозитории
        self.cat_repo = CategoryRepository(conn)
        self.prod_repo = ProductRepository(conn)
        self.size_repo = SizesRepository(conn)
        self.cust_repo = ByerRepository(conn)
        self.order_repo = OrderRepository(conn)
        self.promo_repo = PromoCodeRepository(conn)
        self.addr_repo = AddressRepository(conn)

        # Инициализируем сервисы
        self.catalog_service = CatalogService(self.prod_repo, self.cat_repo, self.size_repo)
        self.cart_service = CartService(self.prod_repo, self.size_repo)
        self.discount_service = DiscountService(self.promo_repo)
        self.order_service = OrderServiceWithDiscount(
            self.order_repo,
            self.prod_repo,
            self.size_repo,
            self.cust_repo,
            self.discount_service
        )

        # Текущий покупатель (для простоты используем id=1)
        self.current_customer_id = 1
        self.current_customer = self.cust_repo.get_by_id_b(self.current_customer_id)

        # Флаг для выхода
        self.running = True

    # --------------------------------------------------------------
    # Вспомогательные методы для ввода и вывода
    # --------------------------------------------------------------

    def _input_int(self, prompt, min_val=None, max_val=None):
        """Безопасный ввод целого числа с проверкой диапазона."""
        while True:
            try:
                value = int(input(prompt).strip())
                if min_val is not None and value < min_val:
                    print(f"Значение должно быть не меньше {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Значение должно быть не больше {max_val}")
                    continue
                return value
            except ValueError:
                print("Введите целое число.")

    def _input_non_empty(self, prompt):
        """Ввод непустой строки."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Поле не может быть пустым.")

    def _print_products(self, products, title="Товары"):
        """Вывод списка товаров."""
        if not products:
            print("Нет товаров.")
            return
        print(f"\n--- {title} ---")
        print(f"{'ID':<4} {'Название':<25} {'Цена':<8} {'Цвет':<10} {'Категория':<15}")
        for p in products:
            cat = self.cat_repo.get_by_id_c(p.category_id)
            cat_name = cat.category_name if cat else "—"
            print(f"{p.id:<4} {p.product_name:<25} {p.price:<8} {p.color:<10} {cat_name:<15}")


# Задание 4
# Реализуйте главное меню.
# Пользователь должен выбирать действия до выхода из программы.


# TODO: добавить главное меню



# Задание 5
# Реализуйте просмотр каталога и поиск товара.
# Вывод должен быть понятным, но бизнес-логика должна оставаться в сервисе.


# TODO: добавить экран каталога и поиска


    def show_catalog(self):
        """Показать все активные товары."""
        products = self.catalog_service.get_active_products()
        self._print_products(products, "Каталог товаров")

    def search_products(self):
        """Поиск товаров по названию."""
        keyword = self._input_non_empty("Введите слово для поиска: ")
        products = self.catalog_service.search_products(keyword)
        if products:
            self._print_products(products, f"Результаты поиска по '{keyword}'")
        else:
            print("Ничего не найдено.")


# Задание 6
# Реализуйте работу с корзиной.
# Добавление, изменение количества, удаление и просмотр суммы должны быть доступны из меню.


# TODO: добавить экран корзины

    def view_cart(self):
        """Показать содержимое корзины."""
        items = self.cart_service.get_cart_items()
        if not items:
            print("Корзина пуста.")
            return

        print("\n--- Ваша корзина ---")
        total = 0
        for idx, item in enumerate(items, 1):
            subtotal = item.price * item.quantity
            total += subtotal
            print(f"{idx}. Товар ID={item.product_id}, размер {item.size}, "
                  f"{item.quantity} шт. по {item.price} руб. = {subtotal} руб.")
        print(f"Итоговая сумма: {total} руб.")
        return total

    def add_to_cart(self):
        """Добавить товар в корзину."""
        try:
            product_id = self._input_int("Введите ID товара: ", min_val=1)
            size = self._input_non_empty("Введите размер (например, 42, M, L): ")
            quantity = self._input_int("Введите количество: ", min_val=1)
            self.cart_service.add_to_cart(product_id, size, quantity)
            print("Товар добавлен в корзину.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def update_cart(self):
        """Изменить количество товара в корзине или удалить."""
        items = self.cart_service.get_cart_items()
        if not items:
            print("Корзина пуста.")
            return

        self.view_cart()
        try:
            idx = self._input_int("Введите номер позиции для изменения (0 для отмены): ", min_val=0)
            if idx == 0:
                return
            if idx < 1 or idx > len(items):
                print("Неверный номер.")
                return
            item = items[idx - 1]
            new_qty = self._input_int("Введите новое количество (0 для удаления): ", min_val=0)
            self.cart_service.update_quantity(item.product_id, item.size, new_qty)
            print("Корзина обновлена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def clear_cart(self):
        """Очистить корзину."""
        if self.cart_service.cart.is_empty():
            print("Корзина уже пуста.")
            return
        confirm = input("Вы уверены, что хотите очистить корзину? (y/n): ").strip().lower()
        if confirm == 'y':
            self.cart_service.clear_cart()
            print("Корзина очищена.")


# Задание 7
# Реализуйте применение промокода и оформление заказа.
# После успешного заказа корзина должна очищаться, заказ сохраняться в PostgreSQL,
# а остатки выбранных размеров уменьшаться.


# TODO: добавить оформление заказа

    def apply_promo(self):
        """Применить промокод (сохраняет в переменной для заказа)."""
        if self.cart_service.cart.is_empty():
            print("Корзина пуста. Добавьте товары сначала.")
            return

        code = self._input_non_empty("Введите код промокода: ")
        try:
            total = self.cart_service.get_cart_total()
            final, discount = self.discount_service.apply_promo(total, code)
            print(f"Промокод применён. Скидка: {discount} руб. Сумма к оплате: {final} руб.")
            # Сохраняем промокод в объекте корзины или в сессии – для простоты сохраним в атрибуте
            self._current_promo = code
        except Exception as e:
            print(f"Ошибка: {e}")
            self._current_promo = None

    def checkout(self):
        """Оформить заказ."""
        if self.cart_service.cart.is_empty():
            print("Корзина пуста. Добавьте товары.")
            return

        # Если промокод был применён, используем его
        promo = getattr(self, '_current_promo', None)
        try:
            order = self.order_service.create_order(self.cart_service, self.current_customer_id, promo)
            print(f"Заказ оформлен! Номер заказа: {order.id}")
            print(f"Сумма до скидки: {order.total_original} руб.")
            print(f"Скидка: {order.discount} руб.")
            print(f"Итоговая сумма: {order.total_final} руб.")
            self._current_promo = None  # сброс после заказа
        except Exception as e:
            print(f"Ошибка оформления заказа: {e}")

    def show_orders(self):
        """Показать историю заказов текущего покупателя."""
        history = self.order_repo.get_order_history(self.current_customer_id)
        if not history:
            print("У вас ещё нет заказов.")
            return

        print("\n--- История заказов ---")
        for order in history:
            print(f"Заказ №{order['id']} от {order['created_at']}")
            print(f"  Статус: {order['status']}")
            print(f"  Сумма: {order['total_final']} руб. (скидка {order['discount']} руб.)")
            print("  Позиции:")
            for item in order['items']:
                print(f"    - {item['product_name']} (размер {item['size']}) x {item['quantity']} = {item['price'] * item['quantity']} руб.")
            print()


    def show_menu(self):
        """Вывод главного меню."""
        print("\n" + "=" * 50)
        print(f"Добро пожаловать, {self.current_customer.byer_name}!")
        print("= Интернет-магазин одежды =")
        print("=" * 50)
        print("1. Просмотр каталога")
        print("2. Поиск товара")
        print("3. Добавить товар в корзину")
        print("4. Просмотр корзины")
        print("5. Изменить корзину")
        print("6. Очистить корзину")
        print("7. Применить промокод")
        print("8. Оформить заказ")
        print("9. История заказов")
        print("0. Выход")
        print("=" * 50)

    def run(self):
        """Запуск основного цикла."""
        # Создаём стартовые данные
        init_data(self.conn)
        self._current_promo = None

        while self.running:
            self.show_menu()
            choice = input("Выберите действие: ").strip()

            if choice == '1':
                self.show_catalog()
            elif choice == '2':
                self.search_products()
            elif choice == '3':
                self.add_to_cart()
            elif choice == '4':
                self.view_cart()
            elif choice == '5':
                self.update_cart()
            elif choice == '6':
                self.clear_cart()
            elif choice == '7':
                self.apply_promo()
            elif choice == '8':
                self.checkout()
            elif choice == '9':
                self.show_orders()
            elif choice == '0':
                print("До свидания!")
                self.running = False
            else:
                print("Неверный ввод. Пожалуйста, выберите пункт меню.")

        self.conn.close()


# ======================================================================
# Точка входа
# ======================================================================

if __name__ == "__main__":
    # Подключаемся к БД
    conn = get_connection()

    # Запускаем приложение
    app = ConsoleApp(conn)
    app.run()


# Задание 8
# Проверьте полный сценарий покупателя и несколько ошибочных сценариев.
# Запишите в комментариях, какие проверки были выполнены вручную.
# После перезапуска программы созданный заказ должен оставаться в базе.


# TODO: провести итоговую ручную проверку
