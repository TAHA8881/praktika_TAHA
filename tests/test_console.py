"""
Тесты консольного интерфейса (этап 08). Используются monkeypatch и capsys.
"""

import pytest
from importlib import import_module

console_app = import_module("17_clothing_store_project.08_console_app")
ClothingStoreApp = console_app.ClothingStoreApp


def test_console_menu_shows_options(capsys, monkeypatch):
    # Подменяем input, чтобы сразу выйти
    monkeypatch.setattr("builtins.input", lambda _: "0")

    app = ClothingStoreApp()
    app.run()

    captured = capsys.readouterr()
    assert "Каталог" in captured.out
    assert "Корзина" in captured.out
    assert "Выход" in captured.out


def test_console_catalog_displays_products(capsys, monkeypatch):
    # Подменяем input, чтобы выбрать каталог, потом выход
    inputs = iter(["1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app = ClothingStoreApp()
    app.run()

    captured = capsys.readouterr()
    assert "Кроссовки" in captured.out  # зависит от тестовых данных