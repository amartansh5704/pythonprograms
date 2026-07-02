-- ============================================
--   PROGRAM 1: E-Commerce Product Catalog
-- ============================================

\c postgres
DROP DATABASE IF EXISTS ecommerce_db;
CREATE DATABASE ecommerce_db;
\c ecommerce_db

-- 1. Create Tables
CREATE TABLE categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    price       DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock       INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL
);

-- 2. Insert Data
INSERT INTO categories (name) VALUES 
('Electronics'), ('Books'), ('Clothing'), ('Home & Kitchen');

INSERT INTO products (name, price, stock, category_id) VALUES
('Laptop', 65000.00, 15, 1),
('Wireless Mouse', 850.00, 120, 1),
('Python Crash Course', 750.00, 45, 2),
('Cotton T-Shirt', 499.00, 200, 3),
('Blender', 3200.00, 8, 4);

-- 3. Practice Queries
-- a) List all products with category name
SELECT p.name, p.price, p.stock, c.name AS category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;

-- b) Find products under ₹1000 with stock > 50
SELECT name, price, stock 
FROM products 
WHERE price < 1000 AND stock > 50;

-- c) Update stock after sale
UPDATE products SET stock = stock - 2 WHERE name = 'Laptop';

-- d) Delete out-of-stock products
DELETE FROM products WHERE stock = 0;

-- e) Verify final state
SELECT * FROM products ORDER BY price DESC;