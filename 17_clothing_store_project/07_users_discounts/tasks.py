"""
Этап 07. Пользователи и скидки

Цель: добавить адреса доставки, промокоды и отдельную логику расчета скидок.
"""

# Задание 1
# Импорты (добавлены репозитории и сервисы из предыдущих этапов)
from importlib import import_module
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# ← Импортируем доменные модели
domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain_models.Product
Category = domain_models.Category
LeftSizes = domain_models.LeftSizes
Byer = domain_models.Byer  # ← используем существующую модель покупателя

# ← Импортируем репозитории из этапа 03
repos = import_module("17_clothing_store_project.03_repositories.tasks")
ProductRepository = repos.ProductRepository
SizesRepository = repos.SizesRepository
ByerRepository = repos.ByerRepository
get_connection = repos.get_connection

# ← Импортируем сервис заказов из этапа 06 (для интеграции скидок)
order_module = import_module("17_clothing_store_project.06_orders.tasks")
OrderService = order_module.OrderService
Order = order_module.Order


# Задание 1 (расширение покупателя – не нужно, используем Byer как есть)
# Вместо создания класса Delivery, мы создаём отдельные модели: Address и PromoCode.

# Задание 3
# Модель адреса доставки
class Address:
    def __init__(self, id=None, customer_id=None, address=None, is_default=False):
        self.id = id
        self.customer_id = customer_id
        self.address = address
        self.is_default = is_default

        # ← простые проверки
        if customer_id is not None and customer_id <= 0:
            raise ValueError("ID покупателя должен быть положительным")
        if address is None or address == "":
            raise ValueError("Адрес не может быть пустым")

    def __str__(self):
        return f"{self.address} (по умолчанию: {self.is_default})"


# Задание 5
# Модель промокода (уже есть, но дополним методом для проверки)
class PromoCode:
    def __init__(self, code, percent, min_total, is_active=True):
        self.code = code
        self.percent = percent
        self.min_total = min_total
        self.is_active = is_active

    # ← метод для проверки применимости
    def is_applicable(self, total):
        return self.is_active and total >= self.min_total


# Задание 4
# Репозиторий адресов
class AddressRepository:
    def __init__(self, connection):
        self.connection = connection

    # ← исправлено: таблица addresses, поля customer_id, address, is_default
    def add(self, address):
        query = """
            INSERT INTO addresses (customer_id, address, is_default)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (address.customer_id, address.address, address.is_default))
            address_id = cursor.fetchone()[0]
            self.connection.commit()
            return address_id

    # ← получение адресов покупателя
    def get_by_customer(self, customer_id):
        query = "SELECT id, customer_id, address, is_default FROM addresses WHERE customer_id = %s ORDER BY is_default DESC"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (customer_id,))
            rows = cursor.fetchall()
            return [Address(row[0], row[1], row[2], row[3]) for row in rows]

    # ← получение адреса по id
    def get_by_id(self, address_id):
        query = "SELECT id, customer_id, address, is_default FROM addresses WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (address_id,))
            row = cursor.fetchone()
            if row:
                return Address(row[0], row[1], row[2], row[3])
            return None

    # ← обновление адреса
    def update(self, address):
        query = "UPDATE addresses SET address = %s, is_default = %s WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (address.address, address.is_default, address.id))
            self.connection.commit()

    # ← удаление адреса
    def delete(self, address_id):
        query = "DELETE FROM addresses WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (address_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Адрес с id {address_id} не найден")
            self.connection.commit()


# Задание 6
# Репозиторий промокодов
class PromoCodeRepository:
    def __init__(self, connection):
        self.connection = connection

    # ← исправлено: таблица promocodes, поля code, percent, min_total, is_active
    def add(self, promo):
        query = """
            INSERT INTO promocodes (code, percent, min_total, is_active)
            VALUES (%s, %s, %s, %s)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (promo.code, promo.percent, promo.min_total, promo.is_active))
            self.connection.commit()

    # ← поиск по коду (регистронезависимый)
    def get_by_code(self, code):
        query = "SELECT code, percent, min_total, is_active FROM promocodes WHERE LOWER(code) = LOWER(%s)"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (code,))
            row = cursor.fetchone()
            if row:
                return PromoCode(row[0], row[1], row[2], row[3])
            return None

    # ← получение всех промокодов
    def get_all(self):
        query = "SELECT code, percent, min_total, is_active FROM promocodes ORDER BY code"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [PromoCode(row[0], row[1], row[2], row[3]) for row in rows]

    # ← обновление промокода
    def update(self, promo):
        query = "UPDATE promocodes SET percent = %s, min_total = %s, is_active = %s WHERE code = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (promo.percent, promo.min_total, promo.is_active, promo.code))
            self.connection.commit()

    # ← удаление промокода
    def delete(self, code):
        query = "DELETE FROM promocodes WHERE code = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (code,))
            if cursor.rowcount == 0:
                raise ValueError(f"Промокод {code} не найден")
            self.connection.commit()


# Задание 7
# Сервис скидок (исправлен, добавляет проверку существования)
class DiscountService:
    def __init__(self, promo_repo):
        self.promo_repo = promo_repo

    def apply_promo(self, total, code):
        if code is None or code == "":
            return total, 0

        promo = self.promo_repo.get_by_code(code)
        if promo is None:
            raise ValueError("Промокод не найден")

        if not promo.is_active:
            raise ValueError("Промокод неактивен")

        if total < promo.min_total:
            raise ValueError(f"Сумма заказа ({total}) меньше минимальной для промокода ({promo.min_total})")

        discount = int(total * promo.percent / 100)
        final = total - discount
        return final, discount


# Задание 8
# Интеграция скидки в заказ – расширяем OrderService из этапа 06
# Для этого создадим новый класс, который наследует OrderService и добавляет применение скидки,
# либо просто переопределим create_order. Мы создадим новый сервис, расширяющий функциональность.

class OrderServiceWithDiscount(OrderService):
    def __init__(self, order_repo, product_repo, sizes_repo, customer_repo, discount_service):
        super().__init__(order_repo, product_repo, sizes_repo, customer_repo)
        self.discount_service = discount_service

    def create_order(self, cart_service, customer_id, promocode=None):
        # ← сначала создаём заказ как обычно (без скидки)
        order = super().create_order(cart_service, customer_id, promocode)
        # ← затем применяем скидку, если промокод передан
        if promocode:
            try:
                final, discount = self.discount_service.apply_promo(order.total_original, promocode)
                order.apply_discount(discount)
                # ← обновляем запись в БД (сохраняем скидку и итоговую сумму)
                self._update_order_totals(order.id, order.total_original, discount, order.total_final)
            except Exception as e:
                # ← если скидка не применилась, откатываем заказ (можно удалить)
                self.order_repo.delete(order.id)  # ← нужно добавить метод delete в OrderRepository
                raise e
        return order

    def _update_order_totals(self, order_id, total_original, discount, total_final):
        query = """
            UPDATE orders SET total_original = %s, discount = %s, total_final = %s
            WHERE id = %s
        """
        with self.order_repo.connection.cursor() as cursor:
            cursor.execute(query, (total_original, discount, total_final, order_id))
            self.order_repo.connection.commit()


# Задание 9 – проверка
if __name__ == "__main__":
    conn = get_connection()

    # Подготавливаем репозитории и сервисы
    product_repo = ProductRepository(conn)
    sizes_repo = SizesRepository(conn)
    customer_repo = ByerRepository(conn)
    order_repo = OrderRepository(conn)
    promo_repo = PromoCodeRepository(conn)
    address_repo = AddressRepository(conn)

    # Создаём тестовые данные
    try:
        # покупатель
        cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
        customer_repo.add_byer(cust)
    except Exception:
        pass

    try:
        # товар
        prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
        product_repo.add_product(prod)
    except Exception:
        pass

    try:
        # остаток
        left = LeftSizes(1, 1, "42", 10)
        sizes_repo.add_left_sizes(left)
    except Exception:
        pass

    try:
        # промокод (скидка 10% при сумме от 1000)
        promo = PromoCode("SALE10", 10, 1000)
        promo_repo.add(promo)
    except Exception:
        pass

    try:
        # адрес
        addr = Address(customer_id=1, address="ул. Ленина, д.1", is_default=True)
        address_repo.add(addr)
    except Exception:
        pass

    # Сервис корзины
    cart_service = CartService(product_repo, sizes_repo)  # ← импортируем из этапа 05
    cart_service.add_to_cart(1, "42", 3)

    # Сервис скидок
    discount_service = DiscountService(promo_repo)

    # Сервис заказов со скидками
    order_service = OrderServiceWithDiscount(order_repo, product_repo, sizes_repo, customer_repo, discount_service)

    # Успешное оформление с промокодом
    try:
        order = order_service.create_order(cart_service, 1, "SALE10")
        print(f"Заказ оформлен, id={order.id}, сумма до скидки={order.total_original}, скидка={order.discount}, итог={order.total_final}")
    except Exception as e:
        print("Ошибка:", e)

    # Проверка сценариев
    # 1. Промокод не найден
    try:
        discount_service.apply_promo(2000, "NONEXIST")
    except Exception as e:
        print("Ожидаемая ошибка (не найден):", e)

    # 2. Промокод неактивен
    try:
        promo_repo.update(PromoCode("SALE10", 10, 1000, is_active=False))
        discount_service.apply_promo(2000, "SALE10")
    except Exception as e:
        print("Ожидаемая ошибка (неактивен):", e)

    # 3. Сумма меньше минимальной
    try:
        promo_repo.update(PromoCode("SALE10", 10, 1000, is_active=True))
        discount_service.apply_promo(500, "SALE10")
    except Exception as e:
        print("Ожидаемая ошибка (меньше минимума):", e)

    conn.close()