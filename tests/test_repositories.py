"""
Интеграционные тесты для репозиториев (03_repositories).
Используется тестовая PostgreSQL-база.
"""

import pytest
from importlib import import_module

domain = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain.Product
Category = domain.Category
LeftSizes = domain.LeftSizes
Byer = domain.Byer


# ---------- CategoryRepository ----------
def test_category_repository_add_and_get(real_category_repo):
    cat = Category(1, "Обувь", "Женская и мужская обувь")
    real_category_repo.add_categories(cat)
    found = real_category_repo.get_by_id_c(1)
    assert found is not None
    assert found.category_name == "Обувь"

def test_category_repository_get_all(real_category_repo):
    cat1 = Category(1, "Обувь", "")
    cat2 = Category(2, "Одежда", "")
    real_category_repo.add_categories(cat1)
    real_category_repo.add_categories(cat2)
    all_cats = real_category_repo.get_all()
    assert len(all_cats) == 2

def test_category_repository_update(real_category_repo):
    cat = Category(1, "Обувь", "Старое описание")
    real_category_repo.add_categories(cat)
    cat.category_description = "Новое описание"
    real_category_repo.update(cat)
    updated = real_category_repo.get_by_id_c(1)
    assert updated.category_description == "Новое описание"

def test_category_repository_delete(real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    real_category_repo.delete(1)
    found = real_category_repo.get_by_id_c(1)
    assert found is None


# ---------- ProductRepository ----------
def test_product_repository_add_and_get(real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные", True)
    real_product_repo.add_product(prod)
    found = real_product_repo.get_by_id_p(1)
    assert found is not None
    assert found.product_name == "Кроссовки"

def test_product_repository_get_all(real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "", True)
    prod2 = Product(2, "Ботинки", 1, 4500, "черный", "", False)
    real_product_repo.add_product(prod1)
    real_product_repo.add_product(prod2)
    all_active = real_product_repo.get_all(only_active=True)
    assert len(all_active) == 1
    all_products = real_product_repo.get_all()
    assert len(all_products) == 2

def test_product_repository_update(real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "", True)
    real_product_repo.add_product(prod)
    prod.product_name = "Новые кроссовки"
    real_product_repo.update(prod)
    updated = real_product_repo.get_by_id_p(1)
    assert updated.product_name == "Новые кроссовки"

def test_product_repository_delete(real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "", True)
    real_product_repo.add_product(prod)
    real_product_repo.delete(1)
    found = real_product_repo.get_by_id_p(1)
    assert found is None

def test_product_repository_get_nonexistent(real_product_repo):
    found = real_product_repo.get_by_id_p(999)
    assert found is None


# ---------- SizesRepository (LeftSizes) ----------
def test_leftsizes_repository_add_and_get(real_size_repo, real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "", True)
    real_product_repo.add_product(prod)
    left = LeftSizes(1, 1, "42", 10)
    real_size_repo.add_left_sizes(left)
    found = real_size_repo.get_by_product_and_size(1, "42")
    assert found is not None
    assert found.quantity == 10

def test_leftsizes_repository_update_quantity(real_size_repo, real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "", True)
    real_product_repo.add_product(prod)
    left = LeftSizes(1, 1, "42", 10)
    real_size_repo.add_left_sizes(left)
    real_size_repo.update_quantity(1, "42", 5)
    found = real_size_repo.get_by_product_and_size(1, "42")
    assert found.quantity == 5

def test_leftsizes_repository_decrease(real_size_repo, real_product_repo, real_category_repo):
    cat = Category(1, "Обувь", "")
    real_category_repo.add_categories(cat)
    prod = Product(1, "Кроссовки", 1, 2500, "белый", "", True)
    real_product_repo.add_product(prod)
    left = LeftSizes(1, 1, "42", 10)
    real_size_repo.add_left_sizes(left)
    real_size_repo.decrease_quantity(1, "42", 3)
    found = real_size_repo.get_by_product_and_size(1, "42")
    assert found.quantity == 7


# ---------- ByerRepository (Customers) ----------
def test_customer_repository_add_and_get(real_customer_repo):
    cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
    real_customer_repo.add_byer(cust)
    found = real_customer_repo.get_by_id_b(1)
    assert found is not None
    assert found.byer_name == "Иван Петров"

def test_customer_repository_get_by_email(real_customer_repo):
    cust = Byer(1, "Иван Петров", "ivan@mail.ru", "+79123456789")
    real_customer_repo.add_byer(cust)
    found = real_customer_repo.get_by_email("ivan@mail.ru")
    assert found is not None

def test_customer_repository_update(real_customer_repo):
    cust = Byer(1, "Иван", "ivan@mail.ru", "+79123456789")
    real_customer_repo.add_byer(cust)
    cust.byer_name = "Иван Петров"
    real_customer_repo.update(cust)
    updated = real_customer_repo.get_by_id_b(1)
    assert updated.byer_name == "Иван Петров"

def test_customer_repository_delete(real_customer_repo):
    cust = Byer(1, "Иван", "ivan@mail.ru", "+79123456789")
    real_customer_repo.add_byer(cust)
    real_customer_repo.delete(1)
    found = real_customer_repo.get_by_id_b(1)
    assert found is None