from flask import Flask, render_template
import os
from dotenv import load_dotenv
from routes import user_bp, product_bp, api_bp
from flask_jwt_extended import JWTManager
load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(api_bp)

app.secret_key = os.getenv('SECRET_KEY_DEV')
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ERROR_MESSAGE_KEY'] = 'msg'

jwt = JWTManager(app)

@app.route('/')
def home():
    print(app.secret_key)
    return render_template('home.html')

if __name__ == "__main__":
    # certificado = os.path.join('certs', 'server.crt')
    # chave = os.path.join('certs', 'server.key')

    # app.run(ssl_context=(certificado, chave), port=5001, debug=True)
    app.run(port=5001, debug=True)