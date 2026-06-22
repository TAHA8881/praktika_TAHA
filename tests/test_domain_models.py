"""
Unit-тесты для доменных моделей (01_domain_models).
Проверяются конструкторы, валидация, изменение состояния.
"""

import pytest
from importlib import import_module

domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes
Byer = domain.Byer


# ---------- Happy path ----------
def test_category_creation():
    cat = Category(1, "Обувь", "Женская и мужская обувь")
    assert cat.category_id == 1
    assert cat.category_name == "Обувь"
    assert cat.category_description == "Женская и мужская обувь"

def test_product_creation():
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    assert prod.id == 1
    assert prod.product_name == "Кроссовки"
    assert prod.category_id == 1
    assert prod.price == 2500
    assert prod.color == "белый"
    assert prod.description == "Спортивные"
    assert prod.is_active is True

def test_left_sizes_creation():
    stock = LeftSizes(1, 1, "XL", 5)
    assert stock.store_id == 1
    assert stock.product_id == 1
    assert stock.size == "XL"
    assert stock.quantity == 5

def test_byer_creation():
    customer = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
    assert customer.byer_id == 1
    assert customer.byer_name == "Иван Петров"
    assert customer.byer_email == "ivan@mail.ru"
    assert customer.byer_telephone == "+79123456789"

def test_product_price_change():
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod.price = 3000
    assert prod.price == 3000

def test_product_activate_deactivate():
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    prod.is_active = False
    assert prod.is_active is False
    prod.is_active = True
    assert prod.is_active is True

def test_left_sizes_quantity_change():
    stock = LeftSizes(1, 1, "XL", 5)
    stock.quantity = 10
    assert stock.quantity == 10

def test_left_sizes_is_available():
    stock = LeftSizes(1, 1, "XL", 5)
    assert stock.is_available() is True
    stock.quantity = 0
    assert stock.is_available() is False


# ---------- Negative path ----------
def test_category_rejects_empty_id():
    with pytest.raises(ValueError, match="Идентификатор"):
        Category("", "Обувь", "Описание")

def test_category_rejects_empty_name():
    with pytest.raises(ValueError, match="Продукт"):
        Category(1, "", "Описание")

def test_product_rejects_negative_id():
    with pytest.raises(ValueError, match="положительным"):
        Product(-1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)

def test_product_rejects_empty_name():
    with pytest.raises(ValueError, match="Название товара"):
        Product(1, "", 1, 2500, "белый", "Спортивные", True)

def test_product_rejects_negative_category_id():
    with pytest.raises(ValueError, match="Категория товара"):
        Product(1, "Кроссовки", -1, 2500, "белый", "Спортивные", True)

def test_product_rejects_negative_price():
    with pytest.raises(ValueError, match="цена продуктов"):
        Product(1, "Кроссовки", 1, -100, "белый", "Спортивные", True)

def test_product_rejects_empty_color():
    with pytest.raises(ValueError, match="Цвет товара"):
        Product(1, "Кроссовки", 1, 2500, "", "Спортивные", True)

def test_product_rejects_empty_description():
    with pytest.raises(ValueError, match="Описание товара"):
        Product(1, "Кроссовки", 1, 2500, "белый", "", True)

def test_leftsizes_rejects_unknown_size():
    with pytest.raises(ValueError, match="Таких размеров одежды нет"):
        LeftSizes(1, 1, "XXX", 5)

def test_leftsizes_rejects_negative_quantity():
    with pytest.raises(ValueError):
        LeftSizes(1, 1, "XL", -5)

def test_byer_rejects_negative_id():
    with pytest.raises(ValueError, match="положительным"):
        Byer(-1, "Иван", "ivan@mail.ru", "+79123456789")

def test_byer_rejects_empty_name():
    with pytest.raises(ValueError, match="Имя покупателя"):
        Byer(1, "", "ivan@mail.ru", "+79123456789")

def test_byer_rejects_invalid_email():
    with pytest.raises(ValueError, match="email"):
        Byer(1, "Иван", "ivanmail.ru", "+79123456789")

def test_byer_rejects_empty_phone():
    with pytest.raises(ValueError, match="Телефон покупателя"):
        Byer(1, "Иван", "ivan@mail.ru", "")


# ---------- Параметризация (Задание 3) ----------
@pytest.mark.parametrize("field_value", ["", "  ", "   "])
def test_product_rejects_whitespace_names(field_value):
    with pytest.raises(ValueError, match="Название товара"):
        Product(1, field_value, 1, 100, "белый", "Описание", True)

@pytest.mark.parametrize("size", ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
def test_leftsizes_rejects_any_unknown_size(size):
    with pytest.raises(ValueError):
        LeftSizes(1, 1, size, 5)

@pytest.mark.parametrize("quantity", [0, -1, -10, -100])
def test_leftsizes_rejects_non_positive_quantity(quantity):
    with pytest.raises(ValueError):
        LeftSizes(1, 1, "XL", quantity)

@pytest.mark.parametrize("email", ["", "no_at", "user@", "@domain", "user@domain."])
def test_byer_rejects_invalid_email_formats(email):
    with pytest.raises(ValueError, match="email"):
        Byer(1, "Иван", email, "+79123456789")

@pytest.mark.parametrize("price", [-1, -100, -0.01])
def test_product_rejects_negative_price(price):
    with pytest.raises(ValueError, match="цена"):
        Product(1, "Товар", 1, price, "белый", "Описание", True)