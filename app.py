from flask import *
import uuid
import os
import database as db
import report as rp
import productAnalisys as pa
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query = db.get_user(db.db_connection(), username)

        if not query or not check_password_hash(query[2], password):
            return redirect('/user/login')

        session['login_user'] = query[0]
        session['user_type'] = query[3] 

        return redirect('/products/listall')

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm-password')
        typeUser = request.form.get('type')

        if password != confirmPassword:
            return redirect('/user/signup')

        idUser = uuid.uuid4()
        password_hash = generate_password_hash(password)
        
        db.insert_user(db.db_connection(), idUser, username, password_hash, typeUser)

        return redirect('/user/login')

@app.route('/user/logout', methods=['GET'])
def logout():
    session.pop('login_user', None)
    return redirect('/')

@app.route('/products/register', methods=['GET', 'POST'])
def register_products():
    if 'login_user' in session:
        if request.method == 'GET':
            return render_template('register-product.html')
        elif request.method == 'POST':
            user_id = session['login_user']
            user_type = session['user_type']

            if user_type == 'standard':
                current_products = db.get_all_products(db.db_connection(), user_id)
                print(current_products)
                if current_products and len(current_products) >= 3:
                    print("Usuários normais só podem cadastrar até 3 produtos.")
                    return redirect('/products/listall')

            nameProduct = request.form.get('name')
            quantity = request.form.get('quantity')
            price = request.form.get('price')

            if not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
                return redirect('/products/register')

            idProduct = uuid.uuid4()
            db.insert_product(db.db_connection(), idProduct, nameProduct, quantity, price, session['login_user'])

            return redirect('/products/listall')
    return redirect('/')

@app.route('/products/listall', methods=['GET'])
def list_products():
    if 'login_user' in session:
        data = db.get_all_products(db.db_connection(), session['login_user'])
        products = [{'name': i[1], 'quantity': i[2], 'price': str(i[3])} for i in data] if data else []
        return render_template('list-all-products.html', products=products)
    return redirect('/')

@app.route('/generate_report', methods=['GET'])
def generate_report_route():
    if 'login_user' in session:
        rp.thread_generate_report(session['login_user'])
        return jsonify({"message": "The report generation has started, you will be notified when it is ready"})
    return redirect('/')

@app.route('/products/analisys/quantity')
def products_analisys_quantity():
    if 'login_user' in session and session['user_type'] == 'admin':
        data = db.get_all_products(db.db_connection(), session['login_user'])
        products = [{'name': i[1], 'quantity': i[2]} for i in data] if data else []
        htmlWithgraphic = pa.quantityAnalisys(products)
        return render_template('quantity-product-analisys.html', graphic_html=htmlWithgraphic)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
