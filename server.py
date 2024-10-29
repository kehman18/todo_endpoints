from flask import Flask, jsonify, request

app = Flask(__name__)

UsersProduct = {
  "users": [
    {
      "user_id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "address": "1234 Elm St, Springfield",
      "age": 30,
      "orders": [101, 102]
    },
    {
      "user_id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "address": "5678 Oak St, Metropolis",
      "age": 25,
      "orders": [103]
    }
  ],
  "orders": [
    {
      "order_id": 101,
      "user_id": 1,
      "total_price": 150.75,
      "products": [1001, 1003]
    },
    {
      "order_id": 102,
      "user_id": 1,
      "total_price": 89.99,
      "products": [1002, 1004]
    },
    {
      "order_id": 103,
      "user_id": 2,
      "total_price": 230.50,
      "products": [1005]
    }
  ],
  "products": [
    {
      "product_id": 1001,
      "name": "Wireless Mouse",
      "category": "Electronics",
      "price": 29.95
    },
    {
      "product_id": 1002,
      "name": "Bluetooth Keyboard",
      "category": "Electronics",
      "price": 49.99
    },
    {
      "product_id": 1003,
      "name": "Gaming Headset",
      "category": "Electronics",
      "price": 89.99
    },
    {
      "product_id": 1004,
      "name": "Smartwatch",
      "category": "Electronics",
      "price": 99.99
    },
    {
      "product_id": 1005,
      "name": "Ergonomic Chair",
      "category": "Furniture",
      "price": 199.99
    }
  ]
}

@app.route('/users', methods=['GET'])
def get_users():
    '''users acct'''
    users = UsersProduct["users"]
    return jsonify(users)

@app.route('/users/<int:id>/total_order_price', methods=['POST'])
def create_orders(id):
    '''function to create orders''' 

    new_products = request.form['products']
    new_price = request.form['price']

    last_order = UsersProduct['orders'][-1]['order_id']
    new_order_id = last_order + 1

    new_order = {
        "order_id": new_order_id,
        "user_id": id,
        "total_price": new_price,
        "products": new_products
    }

    UsersProduct['orders'].append(new_order)

    return jsonify(UsersProduct['orders'])

#get total order price for a user
@app.route('/products/category/<string:category>', methods=['GET'])
def get_products_by_category(category):
    matching_products = [
        product for product in UsersProduct['products'] if product['category'] == category
    ]

    if matching_products:
        return jsonify(matching_products)
    else:
        return jsonify({'message': 'No products found for this category'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')