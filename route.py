from flask import *
import uuid
import database.db_connection as db

app = Flask(__name__)
app.secret_key= 'xcsdKJAH_Sd56$!'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    if 'login_user' in session and 'login_user' != None:
        return render_template('products.html')
    else:
        return render_template('home.html')

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query = db.get_user(db.db_connection(), username, password);

        if query == False:
            return redirect('/user/login')
        
        session['login_user'] = query

        return redirect('/products')

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassowrd = request.form.get('confirm-password')
        typeUser = request.form.get('type')

        idUser = uuid.uuid4()

        if password != confirmPassowrd:
            return redirect('/user/signup')
        
        db.insert_user(db.db_connection(), idUser, username, password, typeUser)

        return redirect('/user/login')

@app.route('/user/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session['login_user'] = None
        return redirect('/user/login')

@app.route('/products/register', methods=['GET', 'POST'])
def register_products():
    if request.method == 'GET' and ('login_user' in session and 'login_user' != None):
        return render_template('register-product.html')
    elif request.method == 'POST'  and ('login_user' in session and 'login_user' != None):
        nameProduct = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        idProduct = uuid.uuid4()
        print(session['login_user'])
        db.insert_product(db.db_connection(), idProduct, nameProduct, quantity, price, session['login_user'])

        return redirect('/products')
    else:
        return redirect('/')

@app.route('/products/listall', methods=['GET'])
def list_products():
    if request.method == 'GET' and ('login_user' in session and 'login_user' != None):
        data = db.get_all_products(db.db_connection(), session['login_user'])

        products = []

        if data != None and data != False:
            for i in data:
                product = {
                'name': i[1],
                'quantity': i[2],
                'price': str(i[3])
                }
                products.append(product)
            
        return render_template('list-all-products.html', products=products)
    
    

if __name__ == "__main__":
    app.run(debug=True)