import sqlite3

conn = sqlite3.connect("oder_lists.sqlite")

cursor = conn.cursor()

sql_query = """ CREATE TABLE order_lists(
    user_id INT PRIMARY KEY,
    name STR NOT NULL,
    email STR NOT NULL,
    age INT,
    orders INT
) """

sql_query = """ ALTER TABLE order_lists ADD COLUMN address VARCHAR(20) """
cursor.execute(sql_query)