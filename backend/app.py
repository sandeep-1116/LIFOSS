import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')), static_url_path='')
CORS(app)

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No MONGO_URI found in environment variables. Please check your .env file.")

client = MongoClient(MONGO_URI)
db = client['ecommerce_db']
products_col = db['products']
users_col = db['users']

# Data Paths (Migration only)
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
USERS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users.json')

def migrate_data():
    """Seed MongoDB if it's empty using local JSON files."""
    if products_col.count_documents({}) == 0:
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r') as f:
                products = json.load(f)
                if products:
                    products_col.insert_many(products)
                    print(f"Migrated {len(products)} products to MongoDB.")

    if users_col.count_documents({}) == 0:
        if os.path.exists(USERS_PATH):
            with open(USERS_PATH, 'r', encoding='utf-8') as f:
                users = json.load(f)
                if users:
                    users_col.insert_many(users)
                    print(f"Migrated {len(users)} users to MongoDB.")

# Perform migration on startup
migrate_data()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login_page():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(products_col.find({}, {'_id': 0}))
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products_col.find_one({'id': product_id}, {'_id': 0})
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# Mock Cart (In-memory for this session)
cart = []

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def manage_cart():
    global cart
    if request.method == 'GET':
        return jsonify(cart)
    
    if request.method == 'POST':
        item = request.json
        product = products_col.find_one({'id': item.get('id')}, {'_id': 0})
        if product:
            existing_item = next((i for i in cart if i['id'] == product['id']), None)
            if existing_item:
                existing_item['quantity'] += 1
            else:
                product_copy = product.copy()
                product_copy['quantity'] = 1
                cart.append(product_copy)
            return jsonify(cart), 201
        return jsonify({"error": "Invalid product"}), 400

    if request.method == 'DELETE':
        cart = []
        return jsonify({"message": "Cart cleared"}), 200

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    if not name or not email or not phone or not password:
        return jsonify({"error": "All fields are required"}), 400
        
    if users_col.find_one({'email': email}):
        return jsonify({"error": "Email already registered"}), 400
    if users_col.find_one({'phone': phone}):
        return jsonify({"error": "Mobile number already registered"}), 400
        
    # Get next ID
    last_user = users_col.find_one(sort=[("id", -1)])
    next_id = (last_user['id'] + 1) if last_user else 1
    
    new_user = {"id": next_id, "name": name, "email": email, "phone": phone, "password": password}
    users_col.insert_one(new_user)
    
    return jsonify({"message": "Account created successfully!", "user": {"name": name, "email": email}}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    user = users_col.find_one({'email': email, 'phone': phone, 'password': password}, {'_id': 0})
    
    if user:
        return jsonify({"message": "Login successful", "user": {"name": user['name'], "email": user['email'], "phone": user.get('phone'), "location": user.get('location'), "pincode": user.get('pincode')}}), 200
        
    return jsonify({"error": "Invalid email or password"}), 401

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    email = data.get('email')
    
    update_data = {
        "name": data.get('name'),
        "phone": data.get('phone'),
        "location": data.get('location'),
        "pincode": data.get('pincode')
    }
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    result = users_col.update_one({'email': email}, {'$set': update_data})
    
    if result.matched_count > 0:
        updated_user = users_col.find_one({'email': email}, {'_id': 0, 'password': 0})
        return jsonify({"message": "Profile synced successfully", "user": updated_user}), 200
        
    return jsonify({"error": "User not found to update."}), 404

otps = {}

@app.route('/api/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    
    user = users_col.find_one({'$or': [{'email': email}, {'phone': phone}]})
    
    if user:
        otp = "123456" 
        otps[user['email']] = otp
        return jsonify({"message": f"OTP sent to your { 'email' if email else 'mobile no' }. (Code: 123456)", "email": user['email']}), 200
        
    return jsonify({"error": "User with this email/phone not found."}), 404

@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')
    
    if otps.get(email) == otp:
        result = users_col.update_one({'email': email}, {'$set': {'password': new_password}})
        if result.matched_count > 0:
            del otps[email]
            return jsonify({"message": "Password reset successful! Please login."}), 200
            
    return jsonify({"error": "Invalid OTP or request."}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"NEON E-Commerce Backend (MongoDB) running on port {port}")
    app.run(debug=False, port=port, host='0.0.0.0')
