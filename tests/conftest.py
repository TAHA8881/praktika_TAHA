"""
Фикстуры для всех тестов.
Используется отдельная тестовая база clothing_store_test.
"""

import os
import pytest
import psycopg2
from importlib import import_module

# ---- Импорт реальных классов из проекта ----
domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes
Byer = domain.Byer

repos = import_module("17_clothing_store_project.03_repositories.tasks")
CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
SizesRepository = repos.SizesRepository
ByerRepository = repos.ByerRepository

catalog_mod = import_module("17_clothing_store_project.04_catalog_service.tasks")
CatalogService = catalog_mod.CatalogService

cart_mod = import_module("17_clothing_store_project.05_cart.tasks")
CartService = cart_mod.CartService

order_mod = import_module("17_clothing_store_project.06_orders.tasks")
OrderRepository = order_mod.OrderRepository
OrderService = order_mod.OrderService

promo_mod = import_module("17_clothing_store_project.07_promocodes.tasks")
DiscountService = promo_mod.DiscountService
PromoCodeRepository = promo_mod.PromoCodeRepository
AddressRepository = promo_mod.AddressRepository
Address = promo_mod.Address
PromoCode = promo_mod.PromoCode
OrderServiceWithDiscount = promo_mod.OrderServiceWithDiscount


# ---- Тестовая БД ----
def get_test_connection():
    """Подключение к тестовой базе."""
    return psycopg2.connect(
        host=os.getenv("TEST_DB_HOST", "localhost"),
        port=os.getenv("TEST_DB_PORT", "5432"),
        dbname=os.getenv("TEST_DB_NAME", "clothing_store_test"),
        user=os.getenv("TEST_DB_USER", "postgres"),
        password=os.getenv("TEST_DB_PASSWORD", "postgres"),
    )


@pytest.fixture(scope="session")
def test_connection():
    """Фикстура подключения к тестовой БД (сессионная)."""
    conn = get_test_connection()
    yield conn
    conn.close()


@pytest.fixture
def clean_db(test_connection):
    """Очищает все таблицы перед каждым интеграционным тестом."""
    with test_connection.cursor() as cur:
        # Порядок важен: сначала дочерние таблицы
        cur.execute("DELETE FROM order_items")
        cur.execute("DELETE FROM orders")
        cur.execute("DELETE FROM leftsizes")
        cur.execute("DELETE FROM products")
        cur.execute("DELETE FROM categories")
        cur.execute("DELETE FROM customers")
        cur.execute("DELETE FROM addresses")
        cur.execute("DELETE FROM promocodes")
    test_connection.commit()
    return test_connection


# ---- Fake-репозитории для unit-тестов ----
class FakeProductRepository:
    def __init__(self, products=None):
        self.products = products or []
        self._next_id = 1

    def add(self, product):
        product.id = self._next_id
        self._next_id += 1
        self.products.append(product)

    def get_by_id(self, product_id):
        for p in self.products:
            if p.id == product_id:
                return p
        return None

    def get_all(self, only_active=False):
        result = self.products
        if only_active:
            result = [p for p in result if p.is_active]
        return result

    def search_by_name(self, keyword, only_active=False):
        keyword = keyword.lower()
        result = self.get_all(only_active)
        return [p for p in result if keyword in p.product_name.lower()]

    def filter_by_category(self, cat_id, only_active=False):
        result = self.get_all(only_active)
        return [p for p in result if p.category_id == cat_id]

    def filter_by_color(self, color, only_active=False):
        color = color.lower()
        result = self.get_all(only_active)
        return [p for p in result if p.color.lower() == color]

    def filter_by_price_range(self, min_p, max_p, only_active=False):
        result = self.get_all(only_active)
        return [p for p in result if min_p <= p.price <= max_p]

    def update(self, product):
        for i, p in enumerate(self.products):
            if p.id == product.id:
                self.products[i] = product
                return
        raise ValueError("Product not found")

    def delete(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]


class FakeCategoryRepository:
    def __init__(self, categories=None):
        self.categories = categories or []
        self._next_id = 1

    def add(self, category):
        category.category_id = self._next_id
        self._next_id += 1
        self.categories.append(category)

    def get_by_id(self, cat_id):
        for c in self.categories:
            if c.category_id == cat_id:
                return c
        return None

    def get_all(self):
        return self.categories


class FakeSizesRepository:
    def __init__(self):
        self.stock = {}  # (product_id, size) -> quantity

    def add(self, leftsize):
        key = (leftsize.product_id, leftsize.size)
        self.stock[key] = leftsize.quantity

    def get_by_product_and_size(self, product_id, size):
        key = (product_id, size)
        qty = self.stock.get(key, 0)
        return LeftSizes(store_id=None, product_id=product_id, size=size, quantity=qty)

    def decrease_quantity(self, product_id, size, amount):
        key = (product_id, size)
        if key not in self.stock:
            raise ValueError("Stock not found")
        if self.stock[key] < amount:
            raise ValueError("Not enough stock")
        self.stock[key] -= amount


# ---- Fixtures для тестов с fake-репозиториями ----
@pytest.fixture
def fake_product_repo():
    return FakeProductRepository()

@pytest.fixture
def fake_category_repo():
    return FakeCategoryRepository()

@pytest.fixture
def fake_size_repo():
    return FakeSizesRepository()

@pytest.fixture
def catalog_service(fake_product_repo, fake_category_repo, fake_size_repo):
    return CatalogService(fake_product_repo, fake_category_repo, fake_size_repo)

@pytest.fixture
def cart_service(fake_product_repo, fake_size_repo):
    return CartService(fake_product_repo, fake_size_repo)


# ---- Фикстуры для интеграционных тестов (реальная БД) ----
@pytest.fixture
def real_category_repo(clean_db):
    return CategoryRepository(clean_db)

@pytest.fixture
def real_product_repo(clean_db):
    return ProductRepository(clean_db)

@pytest.fixture
def real_size_repo(clean_db):
    return SizesRepository(clean_db)

@pytest.fixture
def real_customer_repo(clean_db):
    return ByerRepository(clean_db)

@pytest.fixture
def real_order_repo(clean_db):
    return OrderRepository(clean_db)

@pytest.fixture
def real_promo_repo(clean_db):
    return PromoCodeRepository(clean_db)

@pytest.fixture
def real_catalog_service(real_product_repo, real_category_repo, real_size_repo):
    return CatalogService(real_product_repo, real_category_repo, real_size_repo)

@pytest.fixture
def real_cart_service(real_product_repo, real_size_repo):
    return CartService(real_product_repo, real_size_repo)

@pytest.fixture
def real_discount_service(real_promo_repo):
    return DiscountService(real_promo_repo)

@pytest.fixture
def real_order_service(real_order_repo, real_product_repo, real_size_repo, real_customer_repo):
    return OrderService(real_order_repo, real_product_repo, real_size_repo, real_customer_repo)