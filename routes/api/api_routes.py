from flask import Blueprint, jsonify, request
from database import db_connection, product_dao as pd, user_dao as ud
from utils import is_uuid, generate_uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
import json


api_bp = Blueprint("api", __name__, url_prefix='/api')

@api_bp.route("/users/listall", methods=['GET'])
def json_all_users():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    data = ud.get_users(conn)

    users = []

    for user in data:
        users.append({
            'id': user[0],
            'username': user[1],
            'type': user[3],
        })

    json = {
        'users': users
    }
    return jsonify(json)

@api_bp.route("/users/verifyLogin", methods=['POST'])
def verify_login():
    username = request.json['username']
    password = request.json['password']

    data = ud.get_user(db_connection(), username)

    if not data or not check_password_hash(data[2], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    token = create_access_token(identity=json.dumps({'id': data[0], 'username': data[1], 'type': data[3]}), expires_delta=timedelta(hours=1))
    return jsonify({"token": token}), 200

@api_bp.route('/users/register', methods=['POST'], endpoint = "signup")
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    confirmPassword = request.json.get('confirm-password')
    typeUser = request.json.get('type')

    if password != confirmPassword:
        return jsonify({'error': 'Password is different'}, 401)
    
    if ud.get_user(db_connection(), username):
        return jsonify({'error': 'This user already exist'}, 401)

    idUser = generate_uuid()
    password_hash = generate_password_hash(password)
    
    ud.insert_user(db_connection(), idUser, username, password_hash, typeUser)

    return jsonify({'sucess': 'Registration successful'}), 201

#---------------- API ROUTES PRODUCT --------------------------------
@api_bp.route("/product/listall", methods=['GET'])
def json_all_products():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    data = pd.get_products(conn)

    products = []

    for product in data:
        products.append(
            {   
                'id': product[0],
                'name': product[1],
                'quantity': product[2],
                'price': product[3],
                'userId': product[4]
            }
        )
    
    json = {
        "products": products
    }

    return jsonify(json)

@api_bp.route("/product/getByUser", methods=['GET'])
@jwt_required()
def json_get_product_by_userId():
    conn = db_connection()
    
    current_user = json.loads(get_jwt_identity())

    data = pd.get_product_by_userid(conn, current_user['id'])
    print(data)

    products = []

    for product in data:
        products.append(
            {   
                'id': product[0],
                'name': product[1],
                'quantity': product[2],
                'price': product[3],
            }
        )

    if data:
        response = {
            'status': 'suceeded',
            'data': products
        }
    else:
        response = {
            'status': 'failed',
            'message': 'Product not found'
        }

    return jsonify(response), 200 if data else 400

@api_bp.route("/product/getByProduct/<string:keyProduct>", methods=['GET'])
@jwt_required()
def json_get_product(keyProduct):
    conn = db_connection()
    if is_uuid(keyProduct):
        data = pd.get_product(conn, id=keyProduct)
    else:
        data = pd.get_product(conn, nameProduct=keyProduct)
    
    product = {
        'id': data[0],
        'name': data[1],
        'quantity': data[2],
        'price': str(data[3]),
        'userId': data[4],
    }

    if data:
        response = {
            'status': 'suceeded',
            'product': product
        }
    else:
        response = {
            'status': 'failed',
            'message': 'Product not found'
        }

    return jsonify(response), 200 if data else 400

@api_bp.route("/product/create", methods=['POST'])
@jwt_required()
def json_create_product():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500
    
    product = request.json.get('name')
    quantity = request.json.get('quantity')
    price = request.json.get('price')

    try:
        current_user = json.loads(get_jwt_identity())
        print(f"User identity: {current_user}")
    except Exception as e:
        print(f"Erro ao obter identidade JWT: {e}")
        return jsonify({"error": str(e)}), 401
    
    pd.insert_product(conn, generate_uuid(), product, quantity, price, current_user['id'])

    return jsonify({"success": "Product created successfully"})
