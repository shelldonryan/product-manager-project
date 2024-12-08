from flask import *
import os
from routes import user_bp, product_bp, api_bp

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(api_bp)

app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

@app.route('/')
def home():
    print(app.secret_key)
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
