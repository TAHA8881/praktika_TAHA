"""
Unit-тесты для сервиса каталога (04_catalog_service).
Используются fake-репозитории.
"""

import pytest
from importlib import import_module

domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes

# Фикстуры из conftest.py уже доступны


def test_catalog_returns_only_active_products(catalog_service, fake_product_repo):
    active = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    inactive = Product(2, "Ботинки", 1, 4500, "черный", "Кожаные", False)
    fake_product_repo.products = [active, inactive]

    result = catalog_service.get_active_products()
    assert len(result) == 1
    assert result[0].id == 1


def test_catalog_search_case_insensitive(catalog_service, fake_product_repo):
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    fake_product_repo.products = [prod]

    result = catalog_service.search_products("кросс")
    assert len(result) == 1
    result2 = catalog_service.search_products("КРОСС")
    assert len(result2) == 1


def test_catalog_filter_by_category(catalog_service, fake_product_repo):
    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod2 = Product(2, "Платье", 2, 3500, "красный", "Вечернее", True)
    fake_product_repo.products = [prod1, prod2]

    result = catalog_service.filter_by_category(1)
    assert len(result) == 1
    assert result[0].category_id == 1


def test_catalog_filter_by_color(catalog_service, fake_product_repo):
    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod2 = Product(2, "Платье", 2, 3500, "красный", "Вечернее", True)
    fake_product_repo.products = [prod1, prod2]

    result = catalog_service.filter_by_color("белый")
    assert len(result) == 1
    assert result[0].color == "белый"


def test_catalog_filter_by_size_checks_stock(catalog_service, fake_product_repo, fake_size_repo):
    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod2 = Product(2, "Платье", 2, 3500, "красный", "Вечернее", True)
    fake_product_repo.products = [prod1, prod2]
    # Добавляем остаток только для первого товара
    fake_size_repo.stock[(1, "42")] = 5
    fake_size_repo.stock[(2, "42")] = 0

    result = catalog_service.filter_by_size("42")
    assert len(result) == 1
    assert result[0].id == 1


def test_catalog_filter_by_price_range(catalog_service, fake_product_repo):
    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod2 = Product(2, "Платье", 2, 3500, "красный", "Вечернее", True)
    fake_product_repo.products = [prod1, prod2]

    result = catalog_service.filter_by_price_range(2000, 3000)
    assert len(result) == 1
    assert result[0].price == 2500


def test_catalog_sort_by_price(catalog_service):
    products = [
        Product(1, "Ботинки", 1, 4500, "черный", "", True),
        Product(2, "Кроссовки", 1, 2500, "белый", "", True),
    ]
    sorted_asc = catalog_service.sort_products(products, key="price", reverse=False)
    assert sorted_asc[0].price == 2500
    sorted_desc = catalog_service.sort_products(products, key="price", reverse=True)
    assert sorted_desc[0].price == 4500


def test_catalog_sort_by_name(catalog_service):
    products = [
        Product(1, "Ботинки", 1, 4500, "черный", "", True),
        Product(2, "Кроссовки", 1, 2500, "белый", "", True),
    ]
    sorted_asc = catalog_service.sort_products(products, key="name", reverse=False)
    assert sorted_asc[0].product_name == "Ботинки"
    sorted_desc = catalog_service.sort_products(products, key="name", reverse=True)
    assert sorted_desc[0].product_name == "Кроссовки"


def test_catalog_empty_result(catalog_service, fake_product_repo):
    fake_product_repo.products = []
    result = catalog_service.search_products("несуществующее")
    assert result == []