"""
Тесты для промокодов, адресов и скидок (07_promocodes).
"""

import pytest
from importlib import import_module

promo_mod = import_module("17_clothing_store_project.07_promocodes.tasks")
Address = promo_mod.Address
PromoCode = promo_mod.PromoCode
DiscountService = promo_mod.DiscountService


def test_address_creation():
    addr = Address(1, 1, "ул. Ленина, д.1", True)
    assert addr.id == 1
    assert addr.customer_id == 1
    assert addr.address == "ул. Ленина, д.1"
    assert addr.is_default is True

def test_address_rejects_empty_address():
    with pytest.raises(ValueError, match="Адрес не может быть пустым"):
        Address(1, 1, "")

def test_address_rejects_negative_customer_id():
    with pytest.raises(ValueError, match="положительным"):
        Address(1, -1, "ул. Ленина, д.1")


# ---- Промокоды ----
def test_promo_code_creation():
    promo = PromoCode("SALE10", 10, 1000, True)
    assert promo.code == "SALE10"
    assert promo.percent == 10
    assert promo.min_total == 1000
    assert promo.is_active is True

def test_promo_code_is_applicable():
    promo = PromoCode("SALE10", 10, 1000, True)
    assert promo.is_applicable(1500) is True
    assert promo.is_applicable(900) is False
    promo.is_active = False
    assert promo.is_applicable(1500) is False


# ---- Сервис скидок (используем fake-репозиторий) ----
@pytest.fixture
def fake_promo_repo():
    class FakePromoRepo:
        def __init__(self):
            self.promos = {}
        def get_by_code(self, code):
            return self.promos.get(code)
        def add(self, promo):
            self.promos[promo.code] = promo
    repo = FakePromoRepo()
    repo.add(PromoCode("SALE10", 10, 1000, True))
    repo.add(PromoCode("WELCOME", 15, 500, True))
    repo.add(PromoCode("OLD", 20, 2000, False))
    return repo

def test_discount_service_apply_active_promo(fake_promo_repo):
    service = DiscountService(fake_promo_repo)
    final, discount = service.apply_promo(2000, "SALE10")
    assert final == 1800
    assert discount == 200

def test_discount_service_apply_inactive_promo(fake_promo_repo):
    service = DiscountService(fake_promo_repo)
    with pytest.raises(ValueError, match="неактивен"):
        service.apply_promo(3000, "OLD")

def test_discount_service_apply_unknown_promo(fake_promo_repo):
    service = DiscountService(fake_promo_repo)
    with pytest.raises(ValueError, match="не найден"):
        service.apply_promo(1000, "NONEXIST")

def test_discount_service_rejects_low_sum(fake_promo_repo):
    service = DiscountService(fake_promo_repo)
    with pytest.raises(ValueError, match="меньше минимальной"):
        service.apply_promo(900, "SALE10")

def test_discount_calculation_correct(fake_promo_repo):
    service = DiscountService(fake_promo_repo)
    final, discount = service.apply_promo(1500, "WELCOME")
    assert final == 1275  # 1500 - 15%
    assert discount == 225

def test_discount_final_not_negative(fake_promo_repo):
    service = DiscountService(fake_promo_repo)
    # Предположим, что скидка не может превышать сумму
    # В нашей реализации скидка считается от суммы, значит всегда < 100%
    final, discount = service.apply_promo(100, "WELCOME")  # 15% от 100 = 15
    assert final == 85
    assert discount == 15