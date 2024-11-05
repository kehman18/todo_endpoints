from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server_database.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(60))
    age = db.Column(db.Integer)
    orders = db.relationship('Order', backref='user', lazy=True)

# Order model
class Order(db.Model):
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    products = db.relationship('Product', secondary='order_product', lazy='subquery', backref=db.backref('orders', lazy=True))

# Product model
class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)

# Association table for many-to-many relationship between Orders and Products
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.order_id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
)


UsersProduct = {
  "users": [
    {
      "user_id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "address": "1234 Elm St, Springfield",
      "age": 30,
      "orders": [101]
    },
    {
      "user_id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "address": "5678 Oak St, Metropolis",
      "age": 25,
      "orders": [102]
    },
    {
      "user_id": 3,
      "name": "temiloluwa Oyebefun",
      "email": "oyebefun@example.com",
      "address": "P.O.B 2467 berger, lagos",
      "age": 22,
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
      "user_id": 3,
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

#endpoints to create new users
@app.route('/create_users', methods=['POST'])
def create_user():
    '''create user creates the user'''
    user_data = request.json
    new_user = User(
        name=user_data['name'],
        email=user_data['email'],
        address=user_data.get('address'),
        age=user_data.get('age')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user_id": new_user.user_id}), 201

#create a new products
@app.route('/create_products', methods=['POST'])
def create_product():
    '''the create_product creates a new product'''
    product_data = request.json
    new_product = Product(
        name=product_data['name'],
        category=product_data.get('category'),
        price=product_data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully", "product_id": new_product.product_id}), 201

#crete a new order
@app.route('/create_orders', methods=['POST'])
def create_order():
    order_data = request.json
    user_id = order_data['user_id']
    total_price = order_data['total_price']
    product_ids = order_data['products']

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    products = Product.query.filter(Product.product_id.in_(product_ids)).all()
    if len(products) != len(product_ids):
        return jsonify({"error": "One or more products not found"}), 404

    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        products=products
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully", "order_id": new_order.order_id}), 201

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [
        {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "age": user.age
        }
        for user in users
    ]
    return jsonify(users_data)

# Endpoint to create an order for a specific user
@app.route('/users/<int:id>/total_order_price', methods=['POST'])
def create_orders(id):
    '''create new orders'''
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Parse JSON data from the request
    order_data = request.json
    new_total_price = order_data.get('price')
    new_product_ids = order_data.get('products', [])

    # Create a new order
    new_order = Order(
        user_id=id,
        total_price=new_total_price,
        products=Product.query.filter(Product.product_id.in_(new_product_ids)).all()
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "order_id": new_order.order_id,
        "user_id": new_order.user_id,
        "total_price": new_order.total_price,
        "products": [product.product_id for product in new_order.products]
    })

# Get products by category
@app.route('/products/category/<string:category>', methods=['GET'])
def get_products_by_category(category):
    '''this functions get products by category'''
    matching_products = Product.query.filter_by(category=category).all()
    if not matching_products:
        return jsonify({'message': 'No products found for this category'}), 404

    return jsonify([{
        "product_id": product.product_id,
        "name": product.name,
        "category": product.category,
        "price": product.price
    } for product in matching_products])

# Edit an existing order
@app.route('/products/category/orders/<int:user_id>', methods=['PUT'])
def edit_order(user_id):
    '''edit_order changes the intent of the order of a user'''
    order_data = request.json
    order_id = order_data.get('order_id')

    # Find the user's order
    order = Order.query.filter_by(user_id=user_id, order_id=order_id).first()
    if not order:
        return jsonify({'error': 'Order not found for this user'}), 404

    # Update order details
    order.total_price = order_data.get('total_price', order.total_price)
    new_product_ids = order_data.get('products')
    if new_product_ids:
        order.products = Product.query.filter(Product.product_id.in_(new_product_ids)).all()

    db.session.commit()

    return jsonify({
        "order_id": order.order_id,
        "user_id": order.user_id,
        "total_price": order.total_price,
        "products": [product.product_id for product in order.products]
    })

# Get the highest order for a user
@app.route('/users/<int:user_id>/highest_order', methods=['GET'])
def get_highest_order(user_id):
    '''gets the highest order made by a user'''
    user_orders = Order.query.filter_by(user_id=user_id).order_by(Order.total_price.desc()).all()
    if not user_orders:
        return jsonify({'message': 'User Order not found'}), 404

    highest_order = user_orders[0]
    return jsonify({
        "order_id": highest_order.order_id,
        "total_price": highest_order.total_price,
        "products": [product.product_id for product in highest_order.products]
    })

# Get all users who ordered a product
@app.route('/products/<int:product_id>/users', methods=['GET'])
def get_product_users(product_id):
    '''get all the users who ordered a products'''
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    users = [order.user for order in product.orders]
    if not users:
        return jsonify({'error': 'No users found for the specified product_id'}), 404

    return jsonify([{
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "age": user.age
    } for user in users])

# Get category-wise spending of a user
@app.route('/users/<int:user_id>/spending_by_category', methods=['GET'])
def get_spending_by_category(user_id):
    user_orders = Order.query.filter_by(user_id=user_id).all()
    category_spending = {}

    for order in user_orders:
        for product in order.products:
            category = product.category
            price = product.price
            category_spending[category] = category_spending.get(category, 0) + price

    if not category_spending:
        return jsonify({'error': 'No spending records found for this user'}), 404

    return jsonify(category_spending)

      
# error handler
@app.errorhandler(404)
def page_not_found(error):
   '''treats error for unavailable endpoints'''
   return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
