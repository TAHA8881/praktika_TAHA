"""
Unit-тесты для корзины (05_cart).
"""

import pytest
from importlib import import_module

domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
LeftSizes = domain.LeftSizes

# Фикстуры из conftest


def test_cart_add_product(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    items = cart_service.get_cart_items()
    assert len(items) == 1
    assert items[0].product_id == 1
    assert items[0].size == "42"
    assert items[0].quantity == 2
    assert items[0].price == 2500


def test_cart_same_product_size_increases_quantity(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    cart_service.add_to_cart(1, "42", 3)
    items = cart_service.get_cart_items()
    assert len(items) == 1
    assert items[0].quantity == 5


def test_cart_different_sizes_are_separate_items(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    cart_service.add_to_cart(1, "43", 1)
    items = cart_service.get_cart_items()
    assert len(items) == 2
    assert items[0].size == "42"
    assert items[1].size == "43"


def test_cart_update_quantity(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    cart_service.update_quantity(1, "42", 5)
    items = cart_service.get_cart_items()
    assert items[0].quantity == 5


def test_cart_remove_item(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    cart_service.remove_from_cart(1, "42")
    assert cart_service.cart.is_empty() is True


def test_cart_total_sum(cart_service, fake_product_repo):
    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod2 = Product(2, "Платье", 2, 3500, "красный", "Вечернее", True)
    fake_product_repo.products = [prod1, prod2]
    cart_service.add_to_cart(1, "42", 2)
    cart_service.add_to_cart(2, "M", 1)
    total = cart_service.get_cart_total()
    assert total == 2 * 2500 + 1 * 3500  # 8500


def test_cart_clear(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    cart_service.clear_cart()
    assert cart_service.cart.is_empty() is True


# ---------- Negative path ----------
def test_cart_rejects_zero_quantity(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    with pytest.raises(ValueError, match="положительным"):
        cart_service.add_to_cart(1, "42", 0)


def test_cart_rejects_negative_quantity(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    with pytest.raises(ValueError, match="положительным"):
        cart_service.add_to_cart(1, "42", -1)


def test_cart_rejects_exceeding_stock(cart_service, fake_product_repo, fake_size_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    fake_size_repo.stock[(1, "42")] = 3
    with pytest.raises(ValueError, match="Недостаточно"):
        cart_service.add_to_cart(1, "42", 5)


def test_cart_update_to_invalid_quantity(cart_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]
    cart_service.add_to_cart(1, "42", 2)
    with pytest.raises(ValueError):
        cart_service.update_quantity(1, "42", -5)
    # Проверим, что корзина не изменилась
    items = cart_service.get_cart_items()
    assert items[0].quantity == 2


def test_cart_remove_nonexistent_item(cart_service):
    # Должно быть тихо или предсказуемо (зависит от реализации)
    # Предположим, что remove_from_cart ничего не делает, если товара нет
    cart_service.remove_from_cart(999, "XX")
    assert cart_service.cart.is_empty() is True