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
      "total_price": 89.99,
      "products": [1001, 1003]
    },
    {
      "order_id": 102,
      "user_id": 2,
      "total_price": 150.75,
      "products": [1001, 1004]
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
    '''get products by category'''
    matching_products = [
        product for product in UsersProduct['products'] if product['category'] == category
    ]

    if matching_products:
        return jsonify(matching_products)
    else:
        return jsonify({'message': 'No products found for this category'}), 404


#edit an already existing order
@app.route('/products/category/orders/<int:user_id>', methods=['PUT'])
def add_orders(user_id):
    #get the items of the new orders
    new_order_id = request.form['order_id']
    new_total_price = request.form['total_price']
    new_products = list(request.form['products'])

    check_order = [
        order for order in UsersProduct['orders'] if order['user_id'] == user_id
    ]

    edited_order = {
        check_order['order_id']: new_order_id,
        check_order['user_id']: user_id,
        check_order['total_price']: new_total_price,
        check_order['products']: new_products
    }

    UsersProduct['orders'].append(edited_order)

    return jsonify(UsersProduct['orders'])


#get the user most expensive order
@app.route('/users/<int:user_id>/highest_order', methods=['GET'])
def get_highest_order(user_id):
    '''Function to get the highest order'''

    # Filter the orders by user_id first
    user_orders = [
        order for order in UsersProduct['orders'] if order['user_id'] == user_id
    ]

    # Sort the filtered orders by total_price in descending order
    sorted_user_orders = sorted(user_orders, key=lambda order: order['total_price'], reverse=True)

    if sorted_user_orders:
        return jsonify(sorted_user_orders)
    else:
        return jsonify({'message': 'User Order not found'}), 404


#get all users who ordered a product
@app.route('/products/<int:product_id>/users', methods=['GET'])
def get_product_users(product_id):
    '''Retrieve users who ordered a specific product'''
    
    user_orders = []
    for order in UsersProduct['orders']:
        # Check if product_id is in the list of products for each order
        if product_id in order['products']:
            # Find the user associated with this order's user_id
            for user in UsersProduct['users']:
                if user['user_id'] == order['user_id']:
                    user_orders.append(user)
                    break  # Stop after finding the matching user for this order

    if user_orders:
        return jsonify(user_orders)
    else:
        return jsonify({'error': 'No users found for the specified product_id'}), 404


#get category-wise spending of a user
@app.route('/users/<int:user_id>/spending_by_category', methods=['GET'])
def get_spending_by_category(user_id):
    '''Calculate total spending by category for a specific user'''

    # Dictionary to store spending by category
    category_spending = {}

    # Get orders related to the user
    user_orders = [order for order in UsersProduct['orders'] if order['user_id'] == user_id]

    # For each order, get related products and categorize spending
    for order in user_orders:
        for product_id in order['products']:
            # get the product details by the product_id
            product = next((pro_duct for pro_duct in UsersProduct['products'] if pro_duct['product_id'] == product_id), None)
            
            if product:
                category = product['category']
                price = product['price']
                
                # Sum the price for each category
                if category in category_spending:
                    category_spending[category] += price
                else:
                    category_spending[category] = price

    # Check if there are any spending records; if not, return a 404 error
    if category_spending:
        return jsonify(category_spending)
    else:
        return jsonify({'error': 'No spending records found for this user'}), 404

      
# error handler
@app.errorhandler(404)
def page_not_found(error):
   '''treats error for unavailable endpoints'''
   return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
