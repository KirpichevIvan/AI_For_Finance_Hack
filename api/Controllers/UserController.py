from flask import jsonify, request
from Models.User import User, db
from Models.Role import Role
from Models.Department import Department
from Models.RefreshToken import RefreshToken
from datetime import datetime
from utils.jwt_utils import generate_access_token, generate_refresh_token, decode_access_token
from utils.auth_helpers import authenticate_user, create_new_user, build_auth_response

import json
from flask import jsonify
from flasgger import swag_from

@swag_from({
    'tags': ['Users'],
    'responses': {
        200: {
            'description': 'Список пользователей',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'login': {'type': 'string'},
                                'first_name': {'type': 'string'},
                                'last_name': {'type': 'string'},
                                'password': {'type': 'string'},
                                'roles': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'integer'},
                                            'name': {'type': 'string'}
                                        }
                                    }
                                },
                                'departments': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'integer'},
                                            'name': {'type': 'string'}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_users():
    users = User.query.all()
    output = {
        'status': True if len(users) > 0 else False,
        'message': "OK" if len(users) > 0 else "Empty table",
        'data': []
    }
    for user in users:
        user_roles = [{'id': role.id, 'name': role.name} for role in user.roles]
        user_departments = [{'id': dept.id, 'name': dept.name} for dept in user.departments]
        user_data = {
            'id': user.id, 
            'login': user.login, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'password': user.password,
            'roles': user_roles,
            'departments': user_departments
        }
        output['data'].append(user_data)
    return jsonify(output)


@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID пользователя'
        }
    ],
    'responses': {
        200: {
            'description': 'Информация о пользователе',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'login': {'type': 'string'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'password': {'type': 'string'},
                            'roles': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'}
                                    }
                                }
                            },
                            'departments': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Пользователь не найден',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_user(item_id):
    user = User.query.get(item_id)
    if user:
        user_roles = [{'id': role.id, 'name': role.name} for role in user.roles]
        user_departments = [{'id': dept.id, 'name': dept.name} for dept in user.departments]
        user_data = {
            'id': user.id, 
            'login': user.login, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'password': user.password,
            'roles': user_roles,
            'departments': user_departments
        }
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'User not found'}), 404

"""
method=POST
POST body: login (unique), first_name, last_name, password

returns {
    status: true/false,
    message: OK / Error
    data = inserted user id if success
}
"""
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'login',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Логин пользователя (должен быть уникальным)'
        },
        {
            'name': 'first_name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Имя пользователя'
        },
        {
            'name': 'last_name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Фамилия пользователя'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Пароль пользователя'
        },
        {
            'name': 'role_ids',
            'in': 'formData',
            'type': 'array',
            'required': False,
            'description': 'ID ролей пользователя'
        },
        {
            'name': 'department_ids',
            'in': 'formData',
            'type': 'array',
            'required': False,
            'description': 'ID отделов пользователя'
        }
    ],
    'responses': {
        201: {
            'description': 'Пользователь успешно добавлен',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                }
            }
        },
        400: {
            'description': 'Ошибка в запросе',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        409: {
            'description': 'Пользователь с таким логином уже существует',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def add_user():
    login = request.form.get('login')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    
    # Получаем роли и отделы из запроса
    role_ids = request.form.getlist('role_ids')
    department_ids = request.form.getlist('department_ids')

    if not login or not first_name or not last_name or not password:
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(login=login).first()
    if existing_user:
        return jsonify({'status': False, 'message': 'User with this login already exists'}), 409

    new_user = User(login=login, first_name=first_name, last_name=last_name, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    # Добавляем роли и отделы, если они указаны
    if role_ids:
        for role_id in role_ids:
            role = Role.query.get(role_id)
            if role:
                new_user.roles.append(role)
    
    if department_ids:
        for dept_id in department_ids:
            department = Department.query.get(dept_id)
            if department:
                new_user.departments.append(department)
    
    db.session.commit()
    
    # Получаем ID вставленной записи
    inserted_user_id = new_user.id
    
    return jsonify({'status': True, 'message': 'User added successfully', 'user_id': inserted_user_id}), 201


"""
method=PUT
PUT body: login (unique), first_name, last_name, password

returns {
    status: true/false,
    message: 'User updated successfully' / Error
    data = inserted user id if success
}
"""
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID пользователя для обновления'
        },
        {
            'name': 'login',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Новый логин пользователя'
        },
        {
            'name': 'first_name',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Новое имя пользователя'
        },
        {
            'name': 'last_name',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Новая фамилия пользователя'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Новый пароль пользователя'
        },
        {
            'name': 'role_ids',
            'in': 'formData',
            'type': 'array',
            'required': False,
            'description': 'Обновленный список ID ролей пользователя'
        },
        {
            'name': 'department_ids',
            'in': 'formData',
            'type': 'array',
            'required': False,
            'description': 'Обновленный список ID отделов пользователя'
        }
    ],
    'responses': {
        200: {
            'description': 'Пользователь успешно обновлен',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Пользователь не найден',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        409: {
            'description': 'Пользователь с таким логином уже существует',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def update_user(item_id):
    user = User.query.get(item_id)
    if not user:
        return jsonify({'status': False, 'message': 'User not found'}), 404

    login = request.form.get('login')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    
    # Получаем роли и отделы из запроса
    role_ids = request.form.getlist('role_ids')
    department_ids = request.form.getlist('department_ids')

    if login:
        existing_user = User.query.filter_by(login=login).first()
        if existing_user:
            return jsonify({'status': False, 'message': 'User with this login already exists'}), 409
        user.login = login
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.password = password
        
    # Обновляем роли, если они указаны
    if role_ids is not None:  # Проверяем, что параметр передан (может быть пустым списком)
        user.roles.clear()
        for role_id in role_ids:
            role = Role.query.get(role_id)
            if role:
                user.roles.append(role)
    
    # Обновляем отделы, если они указаны
    if department_ids is not None:  # Проверяем, что параметр передан (может быть пустым списком)
        user.departments.clear()
        for dept_id in department_ids:
            department = Department.query.get(dept_id)
            if department:
                user.departments.append(department)

    db.session.commit()
    return jsonify({'status': True, 'message': 'User updated successfully'})


@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'login',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Логин пользователя'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Пароль пользователя'
        }
    ],
    'responses': {
        200: {
            'description': 'Успешная аутентификация',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'},
                            'refresh_token': {'type': 'string'},
                            'user': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer'},
                                    'login': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Неверные учетные данные',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    result = authenticate_user(login, password)
    
    if 'error' in result and 'status_code' in result:
        return jsonify(result['error']), result['status_code']
    
    response_data, user = result
    return build_auth_response('Login successful', response_data)


@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'refresh_token',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Refresh токен для обновления access токена'
        }
    ],
    'responses': {
        200: {
            'description': 'Токен успешно обновлен',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'},
                            'refresh_token': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Отсутствует refresh токен',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Недействительный или просроченный токен',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Пользователь не найден',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def refresh_token():
    refresh_token_str = request.form.get('refresh_token')
    
    if not refresh_token_str:
        return jsonify({'status': False, 'message': 'Refresh token is required'}), 400
    
    token_record = RefreshToken.query.filter_by(token=refresh_token_str).first()
    
    if not token_record or token_record.is_revoked or token_record.expires_at < datetime.utcnow():
        return jsonify({'status': False, 'message': 'Invalid or expired refresh token'}), 401
    
    user = User.query.get(token_record.user_id)
    if not user:
        return jsonify({'status': False, 'message': 'User not found'}), 404
    
    # Revoke the old refresh token
    token_record.is_revoked = True
    
    # Generate new tokens
    access_token = generate_access_token(user.id)
    new_refresh_token_str = generate_refresh_token()
    
    # Save new refresh token
    new_refresh_token = RefreshToken(token=new_refresh_token_str, user_id=user.id)
    db.session.add(new_refresh_token)
    db.session.commit()
    
    return jsonify({
        'status': True,
        'message': 'Token refreshed successfully',
        'data': {
            'access_token': access_token,
            'refresh_token': new_refresh_token_str
        }
    })


@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'login',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Логин нового пользователя (должен быть уникальным)'
        },
        {
            'name': 'first_name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Имя нового пользователя'
        },
        {
            'name': 'last_name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Фамилия нового пользователя'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Пароль нового пользователя'
        }
    ],
    'responses': {
        201: {
            'description': 'Пользователь успешно зарегистрирован',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'},
                            'refresh_token': {'type': 'string'},
                            'user': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer'},
                                    'login': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Ошибка в запросе',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        409: {
            'description': 'Пользователь с таким логином уже существует',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def register():
    login = request.form.get('login')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    result = create_new_user(login, first_name, last_name, password)
    
    if 'error' in result and 'status_code' in result:
        return jsonify(result['error']), result['status_code']
    
    response_data, user = result
    return build_auth_response('User registered successfully', response_data)
