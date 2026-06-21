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
    is_active BOOLEAN NOT NULL
);

-- TODO: таблица остатков товаров по размерам

CREATE TABLE leftsizes (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    size TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0)
);

-- TODO: таблица покупателей

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL CHECK (email LIKE '%@%'),
	phone TEXT NOT NULL
);

-- Следующие таблицы понадобятся на следующих этапах проекта.

-- TODO: таблица промокодов

CREATE TABLE promocodes (
    code VARCHAR(50) PRIMARY KEY,
    percent INTEGER NOT NULL CHECK (percent BETWEEN 0 AND 100),
    min_total INTEGER NOT NULL CHECK (min_total >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- TODO: таблица адресов доставки

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    address TEXT NOT NULL,
    is_default BOOLEAN DEFAULT FALSE
);

-- TODO: таблица заказов

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    total_original INTEGER NOT NULL CHECK (total_original >= 0),
    discount INTEGER NOT NULL DEFAULT 0 CHECK (discount >= 0),
    total_final INTEGER NOT NULL CHECK (total_final >= 0),
    status TEXT NOT NULL DEFAULT 'создан',
    promocode_used VARCHAR(50) REFERENCES promocodes(code),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);
-- TODO: таблица позиций заказа

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    clothes_id INTEGER NOT NULL REFERENCES products(id),
    clothes_name TEXT NOT NULL,
	size TEXT NOT NULL,
    price NUMERIC(8,2) NOT NULL CHECK(price > 0),
    quantity INTEGER NOT NULL CHECK(quantity > 0)
);