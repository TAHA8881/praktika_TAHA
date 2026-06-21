"""
Этап 05. Корзина

Цель: реализовать добавление товаров в корзину, изменение количества,
удаление позиций и подсчет итоговой суммы.

Модели и сервис корзины создавайте прямо в этом файле.
Товар, остатки и сервис каталога импортируйте из предыдущих этапов.
"""


# Задание 1:)
# Импортируйте модели товара, остатков по размерам и сервис каталога.
# Для проверки создайте несколько товаров с разными остатками по размерам.

# TODO: подготовить товары для корзины

from importlib import import_module
from pathlib import Path
import sys


PROJECT_ROOT = Path (__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain_models.Product
Category = domain_models.Category
LeftSizes = domain_models.LeftSizes
Byer = domain_models.Byer

repos = import_module("17_clothing_store_project.03_repositories.tasks")
ProductRepository = repos.ProductRepository
SizesRepository = repos.SizesRepository
get_connection = repos.get_connection


catalog_module = import_module("17_clothing_store_project.04_catalog_service.tasks")
CatalogService = catalog_module.CatalogService

# Задание 2
# Опишите позицию корзины.
# В позиции должны быть товар, выбранный размер, количество и цена товара.


# TODO: добавить модель позиции корзины
class CartProduct:
    def __init__(self, product_id, size, quantity, price):
        self.product_id = product_id
        self.size = size
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

# Задание 3
# Опишите корзину.
# Она должна хранить набор позиций одного покупателя.
# На этом этапе корзина может жить в памяти текущего запуска программы.


# TODO: добавить модель корзины
class Cart:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        for existing in self._items:
            if existing.product_id == item.product_id and existing.size == item.size:
                existing.quantity += item.quantity
                return
        self._items.append(item)


    def remove_item(self, product_id, size):
        self._items = [it for it in self._items if not (it.product_id == product_id and it.size == size)]


    def update_quantity(self, product_id, size, new_quantity):
        for item in self._items:
            if item.product_id == product_id and item.size == size:
                if new_quantity <= 0:
                    self.remove_item(product_id, size)
                else:
                    item.quantity = new_quantity
                return
        raise ValueError("Товар не найден в корзине")

    def clear(self):
        self._items.clear()

    def get_items(self):
        return self._items

    def total_price(self):
        return sum(item.total() for item in self._items)

    def is_empty(self):
        return len(self._items) == 0



# Задание 4 ✔
# Добавьте добавление товара в корзину.
# Учтите размер, количество и доступный остаток именно выбранного размера.

# TODO: добавить добавление позиции

    
# Задание 5 ✔
# Добавьте изменение количества и удаление позиции.
# Продумайте поведение при нулевом количестве.

    
# TODO: добавить изменение и удаление позиции

# Задание 6 ✔
# Добавьте расчет итоговой суммы и очистку корзины.


# TODO: добавить сумму и очистку корзины


# Задание 7
# При необходимости создайте сервис корзины.
# Он может проверять доступность товара через сервис каталога или репозиторий остатков.

# TODO: отделить бизнес-проверки корзины от пользовательского ввода

class CartService:
    def __init__(self, product_repo, sizes_repo):
        self.product_repo = product_repo
        self.sizes_repo = sizes_repo
        self.cart = Cart()

    def add_to_cart(self, product_id, size, quantity):
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")

        leftover = self.sizes_repo.get_by_product_and_size(product_id, size)
        if leftover is None or leftover.quantity < quantity:
            available = leftover.quantity if leftover else 0
            raise ValueError(f"Недостаточно товара размера {size}. Доступно: {available}")

        product = self.product_repo.get_by_id_p(product_id)
        if product is None:
            raise ValueError(f"Товар с id {product_id} не найден")

        item = CartProduct(product_id, size, quantity, product.price)
        self.cart.add_item(item)

    def remove_from_cart(self, product_id, size):
        self.cart.remove_item(product_id, size)

    def update_quantity(self, product_id, size, new_quantity):
        if new_quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        if new_quantity == 0:
            self.remove_from_cart(product_id, size)
            return

        current_qty = None

        for item in self.cart.get_items():
            if item.product_id == product_id and item.size == size:
                current_qty = item.quantity
                break
        if current_qty is None:
            raise ValueError("Товар не найден в корзине")

        if new_quantity > current_qty:
            leftover = self.sizes_repo.get_by_product_and_size(product_id, size)
            if leftover is None or leftover.quantity < new_quantity:
                available = leftover.quantity if leftover else 0
                raise ValueError(f"Недостаточно товара размера {size}. Доступно: {available}")
        self.cart.update_quantity(product_id, size, new_quantity)

    def get_cart_total(self):
        return self.cart.total_price()

    def clear_cart(self):
        self.cart.clear()

    def get_cart_items(self):
        return self.cart.get_items()

# Задание 8
# Проверьте сценарий: добавить товар, увеличить количество, удалить позицию,
# снова добавить товар и посчитать итог.


# TODO: добавить ручную проверку корзины

if __name__ == "__main__":
    conn = get_connection()
    product_repo = ProductRepository(conn)
    sizes_repo = SizesRepository(conn)

    # Подготовка тестовых данных (если ещё нет)
    # Создаём товар
    try:
        prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные кроссовки", True)
        product_repo.add_product(prod)
    except Exception:
        pass
    # Создаём остаток
    try:
        left = LeftSizes(1, 1, "42", 10)
        sizes_repo.add_left_sizes(left)
    except Exception:
        pass

    # Создаём сервис корзины
    cart_service = CartService(product_repo, sizes_repo)

    print("=== Корзина ===")

    # Добавляем товар
    try:
        cart_service.add_to_cart(1, "42", 2)
        print("Добавлено 2 шт. товара 1 размера 42")
    except Exception as e:
        print("Ошибка:", e)

    # Показываем корзину
    print("Текущая корзина:", [(item.product_id, item.size, item.quantity) for item in cart_service.get_cart_items()])
    print("Итого:", cart_service.get_cart_total())

    # Увеличиваем количество
    try:
        cart_service.update_quantity(1, "42", 5)
        print("Количество изменено на 5")
    except Exception as e:
        print("Ошибка:", e)

    print("Текущая корзина:", [(item.product_id, item.size, item.quantity) for item in cart_service.get_cart_items()])
    print("Итого:", cart_service.get_cart_total())

    # Удаляем позицию
    cart_service.remove_from_cart(1, "42")
    print("Позиция удалена")
    print("Текущая корзина:", [(item.product_id, item.size, item.quantity) for item in cart_service.get_cart_items()])
    print("Итого:", cart_service.get_cart_total())

    # Снова добавляем
    try:
        cart_service.add_to_cart(1, "42", 3)
        print("Добавлено 3 шт.")
    except Exception as e:
        print("Ошибка:", e)

    print("Текущая корзина:", [(item.product_id, item.size, item.quantity) for item in cart_service.get_cart_items()])
    print("Итого:", cart_service.get_cart_total())

    conn.close()