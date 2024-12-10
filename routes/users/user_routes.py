from flask import Blueprint, request, session, render_template, redirect
from database import *
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("users", __name__, url_prefix='/users')

@user_bp.route('/login', methods=['GET', 'POST'], endpoint = "login")
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query = get_user(db_connection(), username)

        if not query or not check_password_hash(query[2], password):
            return redirect('/users/login')

        session['login_user'] = query[0]
        session['user_type'] = query[3]

        return redirect('/product/listall')

@user_bp.route('/signup', methods=['GET', 'POST'], endpoint = "signup")
def signup():
    if request.method == 'GET':
        return render_template('users/signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirm-password')
        typeUser = request.form.get('type')

        if password != confirmPassword:
            return redirect('/users/signup')
        
        if get_user(db_connection(), username):
            return redirect('/users/signup')

        idUser = uuid.uuid4()
        password_hash = generate_password_hash(password)
        
        insert_user(db_connection(), idUser, username, password_hash, typeUser)

        return redirect('/users/login')

@user_bp.route('/logout', methods=['GET'], endpoint='logout')
def logout():
    session.pop('login_user', None)
    return redirect('/')
