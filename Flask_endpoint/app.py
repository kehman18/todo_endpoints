from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Establish connection to SQLite database
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('order_lists.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    '''Home page'''
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM order_lists")
        rows = cursor.fetchall()

        # Construct the response as a list of dictionaries
        order_lists = []
        for row in rows:
            order = {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "address": row[3],
                "age": row[4],
                "orders": row[5]  # This should be stored as an INT in your DB
            }
            order_lists.append(order)

        if order_lists:
            return jsonify(order_lists)
        else:
            return 'No orders found', 404

    if request.method == 'POST':
        # Retrieve form data
        new_user = request.form['name']
        new_email = request.form['email']
        new_address = request.form['address']
        new_age = request.form['age']
        new_orders = request.form['orders']

        sql = """INSERT INTO order_lists (name, email, address, age, orders)
                 VALUES (?, ?, ?, ?, ?)"""
        
        cursor.execute(sql, (new_user, new_email, new_address, new_age, new_orders))
        conn.commit()

        return f'Order with ID: {cursor.lastrowid} created successfully', 201

@app.route('/home/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def edit_page(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM order_lists WHERE user_id=?", (id,))
        row = cursor.fetchone()

        if row is not None:
            order = {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "address": row[3],
                "age": row[4],
                "orders": row[5]
            }
            return jsonify(order)
        return 'User not found', 404
    
    if request.method == 'PUT':
        cursor.execute("SELECT * FROM order_lists WHERE user_id=?", (id,))
        row = cursor.fetchone()
        
        if row is not None:
            updated_user = request.form['name']
            updated_email = request.form['email']
            updated_address = request.form['address']
            updated_age = request.form['age']
            updated_orders = request.form['orders']

            sql = """UPDATE order_lists
                     SET name=?, email=?, address=?, age=?, orders=?
                     WHERE user_id=?"""
            cursor.execute(sql, (updated_user, updated_email, updated_address, updated_age, updated_orders, id))
            conn.commit()

            return f'User with ID: {id} updated successfully', 200
        return 'User not found', 404

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM order_lists WHERE user_id=?", (id,))
        conn.commit()

        return f'User with ID: {id} deleted successfully', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
