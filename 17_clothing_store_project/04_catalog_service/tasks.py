"""
Этап 04. Сервис каталога

Цель: вынести логику просмотра, поиска и фильтрации товаров в отдельный
сервисный слой.

Сервис каталога создавайте прямо в этом файле.
Репозитории импортируйте из 03_repositories/tasks.py.
"""

# Задание 1
# Импортируйте модели, репозитории товаров, категорий и остатков по размерам.
# Добавьте несколько товаров разных категорий, цветов, размеров, цен и остатков.

# TODO: добавить сервис каталога

import os
import psycopg2
from importlib import import_module
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


domain_models = import_module("17_clothing_store_project.01_domain_models.tasks")
Product = domain_models.Product
Category = domain_models.Category
LeftSizes = domain_models.LeftSizes
Byer = domain_models.Byer


repos = import_module("17_clothing_store_project.03_repositories.tasks")
CategoryRepository = repos.CategoryRepository
ProductRepository = repos.ProductRepository
SizesRepository = repos.SizesRepository
ByerRepository = repos.ByerRepository
get_connection = repos.get_connection

# Задание 2
# Создайте сервис каталога, который получает репозиторий товаров.
# При необходимости передайте в сервис репозиторий категорий и репозиторий остатков.
# Сервис должен работать через методы репозиториев, а не через внешний список.

# TODO: добавить сервис каталога

class CatalogService:
    def __init__(self, product_repo, category_repo, sizes_repo):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.sizes_repo = sizes_repo

# Задание 3
# Добавьте получение активных товаров.
# Неактивные товары не должны попадать в обычную выдачу каталога.


# TODO: добавить выдачу активных товаров

    def get_active_products(self):  
        return self.product_repo.get_all(only_active=True)

# Задание 4
# Добавьте поиск по части названия.
# Поиск должен быть удобным для пользователя и не зависеть от регистра.


# TODO: добавить поиск по названию

    def search_products(self, keyword):  
        return self.product_repo.search_by_name(keyword, only_active=True)

# Задание 5
# Добавьте фильтрацию по категории ✔ , размеру ✔, цвету ✔ и диапазону цены ✔ .
# Фильтр по размеру должен учитывать наличие товара именно этого размера.
# Фильтры можно реализовать постепенно.


# TODO: добавить фильтрацию каталога
    def filter_by_category(self, category_id):  
        return self.product_repo.filter_by_category(category_id, only_active=True)

    def filter_by_color(self, color):   
        return self.product_repo.filter_by_color(color, only_active=True)

    def filter_by_price_range(self, min_price, max_price):  
        return self.product_repo.filter_by_price_range(min_price, max_price, only_active=True)

    def filter_by_size(self, size):   
        products = self.product_repo.get_all(only_active=True)
        result = []
        for p in products:
            left = self.sizes_repo.get_by_product_and_size(p.id, size)
            if left and left.quantity > 0:
                result.append(p)
        return result

    # комбинированный фильтр (все параметры опциональны)
    def filter_products(self, category_id=None, color=None,
                        min_price=None, max_price=None, size=None):
        products = self.product_repo.get_all(only_active=True)
        if category_id is not None:
            products = [p for p in products if p.category_id == category_id]
        if color is not None:
            products = [p for p in products if p.color.lower() == color.lower()]
        if min_price is not None:
            products = [p for p in products if p.price >= min_price]
        if max_price is not None:
            products = [p for p in products if p.price <= max_price]
        if size is not None:
            filtered = []
            for p in products:
                left = self.sizes_repo.get_by_product_and_size(p.id, size)
                if left and left.quantity > 0:
                    filtered.append(p)
            products = filtered
        return products

# Задание 6
# Добавьте сортировку найденных товаров.
# Продумайте варианты сортировки по цене и названию.


# TODO: добавить сортировку каталога

    def sort_products(self, products, key='price', reverse=False):
        if key == 'price':
            return sorted(products, key=lambda p: p.price, reverse=reverse)
        elif key == 'name':
            return sorted(products, key=lambda p: p.product_name.lower(), reverse=reverse)
        else:
            raise ValueError("Ключ сортировки должен быть 'price' или 'name'")


# Задание 7
# Проверьте сервис на нескольких сценариях поиска и фильтрации.
if __name__ == "__main__":
    conn = get_connection()

    # Создаём репозитории
    cat_repo = CategoryRepository(conn)
    prod_repo = ProductRepository(conn)
    size_repo = SizesRepository(conn)

    #Создаём сервис каталога
    catalog = CatalogService(prod_repo, cat_repo, size_repo)

    # Подготовка тестовых данных 
    try:
        cat1 = Category(1, "Обувь", "Женская и мужская обувь")
        cat_repo.add_categories(cat1)
    except Exception:
        pass

    try:
        cat2 = Category(2, "Одежда", "Верхняя одежда, платья")
        cat_repo.add_categories(cat2)
    except Exception:
        pass

    try:
        prod1 = Product(1, "Кроссовки", 1, 2500, "белый", "Спортивные кроссовки", True)
        prod_repo.add_product(prod1)
    except Exception:
        pass

    try:
        prod2 = Product(2, "Платье", 2, 3500, "красный", "Вечернее платье", True)
        prod_repo.add_product(prod2)
    except Exception:
        pass

    try:
        prod3 = Product(3, "Ботинки", 1, 4500, "черный", "Кожаные ботинки", False)
        prod_repo.add_product(prod3)
    except Exception:
        pass

    try:
        size1 = LeftSizes(1, 1, "42", 10)
        size_repo.add_left_sizes(size1)
    except Exception:
        pass

    try:
        size2 = LeftSizes(2, 1, "43", 5)
        size_repo.add_left_sizes(size2)
    except Exception:
        pass

    try:
        size3 = LeftSizes(3, 2, "M", 7)
        size_repo.add_left_sizes(size3)
    except Exception:
        pass

    #Проверки
    print("=== 1. Все активные товары ===")
    active = catalog.get_active_products()
    for p in active:
        print(f"{p.id}: {p.product_name} ({p.color}) - {p.price} руб.")

    print("\n=== 2. Поиск по названию 'кросс' ===")
    found = catalog.search_products("кросс")
    for p in found:
        print(f"{p.id}: {p.product_name}")

    print("\n=== 3. Фильтр по категории (id=1 - Обувь) ===")
    by_cat = catalog.filter_by_category(1)
    for p in by_cat:
        print(f"{p.id}: {p.product_name}")

    print("\n=== 4. Фильтр по цвету 'красный' ===")
    by_color = catalog.filter_by_color("красный")
    for p in by_color:
        print(f"{p.id}: {p.product_name}")

    print("\n=== 5. Фильтр по диапазону цен 2000-4000 ===")
    by_price = catalog.filter_by_price_range(2000, 4000)
    for p in by_price:
        print(f"{p.id}: {p.product_name} - {p.price}")

    print("\n=== 6. Фильтр по размеру '42' ===")
    by_size = catalog.filter_by_size("42")
    for p in by_size:
        print(f"{p.id}: {p.product_name} - размер 42")

    print("\n=== 7. Комбинированный фильтр (категория=1, цена от 2000 до 3000) ===")
    combined = catalog.filter_products(category_id=1, min_price=2000, max_price=3000)
    for p in combined:
        print(f"{p.id}: {p.product_name} - {p.price}")

    print("\n=== 8. Сортировка по цене (возрастание) ===")
    sorted_by_price = catalog.sort_products(active, key='price')
    for p in sorted_by_price:
        print(f"{p.id}: {p.product_name} - {p.price}")

    print("\n=== 9. Сортировка по названию (алфавит) ===")
    sorted_by_name = catalog.sort_products(active, key='name')
    for p in sorted_by_name:
        print(f"{p.id}: {p.product_name}")

    conn.close()