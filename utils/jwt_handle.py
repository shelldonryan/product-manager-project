from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

load_dotenv()

def generate_jwt(user_id, user_role):
    expiration = datetime.now () + timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'user_role': user_role,
        'exp': expiration,
    }
    token = encode(payload, os.getenv("SECRET_KEY_DEV"), algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        decoded = jwt.decode(token, os.getenv("SECRET_KEY_DEV"), algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
