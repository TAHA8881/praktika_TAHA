-- Этап 02. SQL-схема проекта
-- Здесь студенты описывают таблицы PostgreSQL для интернет-магазина одежды.
-- Файл не содержит готового решения: используйте его как место для своей схемы.

-- TODO: таблица категорий

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL 
);
-- TODO: таблица товаров

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0),
    color VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    is_active boolean not null
);

-- TODO: таблица остатков товаров по размерам

CREATE TABLE leftsizes (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    size TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0)
);

-- TODO: таблица покупателей
CREATE TABLE byer (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL CHEK(email != '@'),
	phone TEXT NOT NULL
);

-- Следующие таблицы понадобятся на следующих этапах проекта.

-- TODO: таблица заказов
CREATE TABLE order (
    id INTEGER PRIMARY KEY,
    users_id INTEGER NOT NULL REFERENCES users(id),
    total INTEGER NOT NULL CHEK(TOTAL >= 0),
	status TEXT NOT NULL
);
-- TODO: таблица позиций заказа

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES order(id),
    clothes_id INTEGER NOT NULL REFERENCES order(id),
    clothes_name TEXT NOT NULL,
	size TEXT NOT NULL,
   quantity INTEGER NOT NULL (quantity = 0),
);
-- TODO: таблица адресов доставки

-- TODO: таблица промокодов

