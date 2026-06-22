"""
Интеграционный тест полного пользовательского сценария.
"""

import pytest
from importlib import import_module

domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes
Byer = domain.Byer
PromoCode = import_module("17_clothing_store_project.07_promocodes.tasks").PromoCode


def test_full_scenario(real_category_repo, real_product_repo, real_size_repo,
                       real_customer_repo, real_promo_repo, real_order_repo,
                       real_catalog_service, real_cart_service, real_discount_service,
                       real_order_service):
    """
    1. Создать тестовые данные.
    2. Найти активные товары.
    3. Найти товар по названию.
    4. Добавить в корзину.
    5. Изменить количество.
    6. Применить промокод.
    7. Оформить заказ.
    8. Проверить сохранённый заказ.
    9. Проверить уменьшение остатков.
    """

    # ---- 1. Создаём данные ----
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)

    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod2 = Product(2, "Ботинки", 1, 4500, "черный", "Кожаные", True)
    real_product_repo.add_product(prod1)
    real_product_repo.add_product(prod2)

    left1 = LeftSizes(1, 1, "42", 10)
    left2 = LeftSizes(2, 2, "43", 5)
    real_size_repo.add_left_sizes(left1)
    real_size_repo.add_left_sizes(left2)

    cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
    real_customer_repo.add_byer(cust)

    promo = PromoCode("SALE10", 10, 2000, True)
    real_promo_repo.add(promo)

    # ---- 2. Каталог: активные товары ----
    active = real_catalog_service.get_active_products()
    assert len(active) == 2

    # ---- 3. Поиск ----
    found = real_catalog_service.search_products("кросс")
    assert len(found) == 1
    assert found[0].id == 1

    # ---- 4. Добавление в корзину ----
    real_cart_service.add_to_cart(1, "42", 2)
    assert len(real_cart_service.get_cart_items()) == 1

    # ---- 5. Изменение количества ----
    real_cart_service.update_quantity(1, "42", 3)
    items = real_cart_service.get_cart_items()
    assert items[0].quantity == 3

    # ---- 6. Применение промокода ----
    total = real_cart_service.get_cart_total()  # 3*2500 = 7500
    final, discount = real_discount_service.apply_promo(total, "SALE10")
    assert final == 6750
    assert discount == 750

    # ---- 7. Оформление заказа ----
    order = real_order_service.create_order(real_cart_service, customer_id=1, promocode="SALE10")
    assert order is not None
    assert order.total_final == 6750
    assert order.discount == 750

    # ---- 8. Проверка сохранённого заказа ----
    history = real_order_repo.get_order_history(1)
    assert len(history) == 1
    assert history[0]["id"] == order.id
    assert history[0]["total_final"] == 6750

    # ---- 9. Проверка остатков ----
    stock = real_size_repo.get_by_product_and_size(1, "42")
    assert stock.quantity == 7  # было 10, списано 3

    # Корзина очищена
    assert real_cart_service.cart.is_empty() is True