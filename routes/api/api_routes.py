from flask import Blueprint, jsonify, request
from database import db_connection, product_dao as pd, user_dao as ud
from utils import is_uuid, generate_uuid
from werkzeug.security import generate_password_hash, check_password_hash


api_bp = Blueprint("api", __name__, url_prefix='/api')

@api_bp.route("/user/listall", methods=['GET'])
def json_all_users():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    data = ud.get_users(conn)

    users = []

    for user in data:
        users.api_bpend({
            'id': user[0],
            'username': user[1],
            'type': user[3],
        })

    json = {
        'users': users
    }
    return jsonify(json)

@api_bp.route("/user/verifyLogin")
def verify_login():
    username = request.json['username']
    password = request.json['password']

    data = ud.get_user(db_connection(), username)

    if not data or not check_password_hash(data[2], password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return jsonify({'id': data[0], 'username': data[1], 'password': data[2], 'type': data[3]}), 200

@api_bp.route('/user/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    typeUser = request.json['type']

    if ud.get_user(db_connection(), username):
        return jsonify({'error': 'Username already exists'}), 409
    
    idUser = generate_uuid()
    hashed_password = generate_password_hash(password)

    ud.add_user(db_connection(), idUser, username, hashed_password, typeUser)

    return jsonify({'id': idUser, 'username': username, 'password': password, 'type': typeUser}), 201


#---------------- API ROUTES PRODUCT --------------------------------
@api_bp.route("/product/listall", methods=['GET'])
def json_all_products():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    data = pd.get_products(conn)

    products = []

    for product in data:
        products.api_bpend(
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

@api_bp.route("/product/getByUser/<string:userId>", methods=['GET'])
def json_get_product_by_userId(userId):
    conn = db_connection()
    
    data = pd.get_product_by_userid(conn, userId)
    print(data)

    products = []

    for product in data:
        products.api_bpend(
            {   
                'id': product[0],
                'name': product[1],
                'quantity': product[2],
                'price': product[3],
                'userId': product[4]
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
def json_create_product():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500
    
    product = request.json["name"]
    quantity = request.json["quantity"]
    price = request.json["price"]

    pd.add_product(conn, product, quantity, price)

    return jsonify({"success": "Product created successfully"})
