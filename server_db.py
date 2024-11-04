import sqlite3

conn = sqlite3.connect("server_db.sqlite")

cursor = conn.cursor()

sql_query = """ CREATE TABLE users(
    user_id INT PRIMARY KEY UNIQUE,
    name STR NOT NULL,
    email STR NOT NULL,
    age INT,
    orders INT
) 

CREATE TABLE orders(
    order_id INT,
    user_id INT FOREIGN KEY,
    total_price INT,
    products INT
)

CREATE TABLE products(
    product_id INT,
    name VARCHAR(40),
    category VARCHAR(30),
    price int
)
"""

cursor.execute(sql_query)

































