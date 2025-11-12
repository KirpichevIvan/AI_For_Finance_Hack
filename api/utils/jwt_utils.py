import uuid
from datetime import datetime, timedelta
import jwt
from functools import wraps

SECRET_KEY = "your-secret-key-here"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def generate_access_token(user_id):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def generate_refresh_token():
    return str(uuid.uuid4())

def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, jsonify
        
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': False, 'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = decode_access_token(token)
            if not payload:
                return jsonify({'status': False, 'message': 'Token is invalid or expired'}), 401
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'status': False, 'message': 'Token validation failed'}), 401
    
    return decorated