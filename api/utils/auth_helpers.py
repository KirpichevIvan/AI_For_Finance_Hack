from flask import jsonify
from Models.User import User, db
from Models.RefreshToken import RefreshToken
from datetime import datetime
from utils.jwt_utils import generate_access_token, generate_refresh_token

def authenticate_user(login, password):
    if not login or not password:
        return {'error': {'status': False, 'message': 'Missing login or password'}, 'status_code': 400}
    
    user = User.query.filter_by(login=login).first()
    if not user or not user.check_password(password):
        return {'error': {'status': False, 'message': 'Invalid credentials'}, 'status_code': 401}
    
    access_token = generate_access_token(user.id)
    refresh_token_str = generate_refresh_token()
    
    refresh_token = RefreshToken(token=refresh_token_str, user_id=user.id)
    db.session.add(refresh_token)
    db.session.commit()
    
    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token_str,
        'user': {
            'id': user.id,
            'login': user.login,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }
    
    return response_data, user

def create_new_user(login, first_name, last_name, password):
    if not login or not first_name or not last_name or not password:
        return {'error': {'status': False, 'message': 'Missing required fields'}, 'status_code': 400}
    
    existing_user = User.query.filter_by(login=login).first()
    if existing_user:
        return {'error': {'status': False, 'message': 'User with this login already exists'}, 'status_code': 409}
    
    new_user = User(login=login, first_name=first_name, last_name=last_name, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    user_id = new_user.id
    access_token = generate_access_token(user_id)
    refresh_token_str = generate_refresh_token()
    
    refresh_token = RefreshToken(token=refresh_token_str, user_id=user_id)
    db.session.add(refresh_token)
    db.session.commit()
    
    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token_str,
        'user': {
            'id': new_user.id,
            'login': new_user.login,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name
        }
    }
    
    return response_data, new_user

def build_auth_response(message, response_data):
    return jsonify({
        'status': True,
        'message': message,
        'data': response_data
    })