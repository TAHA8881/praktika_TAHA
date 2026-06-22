"""
Интеграционные тесты для сервиса заказов (06_orders + 07_promocodes).
Проверяются транзакции и списание остатков.
"""

import pytest
from importlib import import_module

domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes
Byer = domain.Byer

# Используем реальные репозитории и сервисы с тестовой БД


def prepare_test_data(real_category_repo, real_product_repo, real_size_repo, real_customer_repo):
    """Вспомогательная функция для подготовки данных."""
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)

    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    real_product_repo.add_product(prod)

    left = LeftSizes(1, 1, "42", 10)
    real_size_repo.add_left_sizes(left)

    cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
    real_customer_repo.add_byer(cust)


def test_order_creation_happy_path(real_order_service, real_cart_service, real_category_repo,
                                   real_product_repo, real_size_repo, real_customer_repo,
                                   real_order_repo):
    prepare_test_data(real_category_repo, real_product_repo, real_size_repo, real_customer_repo)

    # Добавляем товар в корзину
    real_cart_service.add_to_cart(1, "42", 3)
    order = real_order_service.create_order(real_cart_service, customer_id=1)

    assert order is not None
    assert order.id is not None
    assert order.total_final == 3 * 2500  # 7500
    assert order.status == "создан"
    assert len(order.items) == 1

    # Проверяем, что остаток уменьшился
    stock_after = real_size_repo.get_by_product_and_size(1, "42")
    assert stock_after.quantity == 7

    # Корзина должна очиститься
    assert real_cart_service.cart.is_empty() is True


def test_order_rejects_empty_cart(real_order_service, real_cart_service):
    with pytest.raises(ValueError, match="Корзина пуста"):
        real_order_service.create_order(real_cart_service, customer_id=1)


def test_order_rejects_unknown_customer(real_order_service, real_cart_service, real_category_repo,
                                        real_product_repo, real_size_repo):
    # Подготовим данные без покупателя
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    real_product_repo.add_product(prod)
    left = LeftSizes(1, 1, "42", 10)
    real_size_repo.add_left_sizes(left)

    real_cart_service.add_to_cart(1, "42", 3)
    with pytest.raises(ValueError, match="Покупатель с id"):
        real_order_service.create_order(real_cart_service, customer_id=999)


def test_order_rejects_insufficient_stock(real_order_service, real_cart_service, real_category_repo,
                                          real_product_repo, real_size_repo, real_customer_repo):
    prepare_test_data(real_category_repo, real_product_repo, real_size_repo, real_customer_repo)
    real_cart_service.add_to_cart(1, "42", 20)  # доступно только 10
    with pytest.raises(ValueError, match="Недостаточно товара"):
        real_order_service.create_order(real_cart_service, customer_id=1)

    # Проверяем, что остаток не изменился
    stock = real_size_repo.get_by_product_and_size(1, "42")
    assert stock.quantity == 10
    assert not real_cart_service.cart.is_empty()  # корзина не очищена


def test_order_transaction_rollback_on_error(real_order_service, real_cart_service, real_category_repo,
                                             real_product_repo, real_size_repo, real_customer_repo,
                                             real_order_repo, monkeypatch):
    """
    Проверяем, что при ошибке во время оформления (например, сбой списания)
    заказ не сохраняется и остатки не меняются.
    """
    prepare_test_data(real_category_repo, real_product_repo, real_size_repo, real_customer_repo)
    real_cart_service.add_to_cart(1, "42", 3)

    # Симулируем ошибку в репозитории остатков
    def failing_decrease(*args, **kwargs):
        raise Exception("Ошибка базы данных")

    monkeypatch.setattr(real_size_repo, "decrease_quantity", failing_decrease)

    with pytest.raises(Exception, match="Ошибка базы данных"):
        real_order_service.create_order(real_cart_service, customer_id=1)

    # Проверяем, что заказ не сохранён
    orders = real_order_repo.get_order_history(1)
    assert len(orders) == 0

    # Остатки не изменились
    stock = real_size_repo.get_by_product_and_size(1, "42")
    assert stock.quantity == 10

    # Корзина не очищена
    assert not real_cart_service.cart.is_empty()