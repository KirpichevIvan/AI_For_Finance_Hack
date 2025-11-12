from flask import jsonify, request
from Models.Role import Role, db
from flasgger import swag_from

@swag_from({
    'tags': ['Roles'],
    'responses': {
        200: {
            'description': 'Список ролей',
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
                                'name': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_roles():
    roles = Role.query.all()
    output = {
        'status': True if len(roles) > 0 else False,
        'message': "OK" if len(roles) > 0 else "Empty table",
        'data': []
    }
    for role in roles:
        role_data = {'id': role.id, 'name': role.name}
        output['data'].append(role_data)
    return jsonify(output)


@swag_from({
    'tags': ['Roles'],
    'parameters': [
        {
            'name': 'role_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID роли'
        }
    ],
    'responses': {
        200: {
            'description': 'Информация о роли',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'}
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Роль не найдена',
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
def get_role(role_id):
    role = Role.query.get(role_id)
    if role:
        role_data = {'id': role.id, 'name': role.name}
        return jsonify({'status': True, 'message': 'OK', 'data': role_data})
    else:
        return jsonify({'status': False, 'message': 'Role not found'}), 404


@swag_from({
    'tags': ['Roles'],
    'parameters': [
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Название роли (должно быть уникальным)'
        }
    ],
    'responses': {
        201: {
            'description': 'Роль успешно создана',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'role_id': {'type': 'integer'}
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
            'description': 'Роль с таким названием уже существует',
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
def add_role():
    name = request.form.get('name')

    if not name:
        return jsonify({'status': False, 'message': 'Missing required field: name'}), 400

    existing_role = Role.query.filter_by(name=name).first()
    if existing_role:
        return jsonify({'status': False, 'message': 'Role with this name already exists'}), 409

    new_role = Role(name=name)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({'status': True, 'message': 'Role added successfully', 'role_id': new_role.id}), 201


@swag_from({
    'tags': ['Roles'],
    'parameters': [
        {
            'name': 'role_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID роли для обновления'
        },
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Новое название роли'
        }
    ],
    'responses': {
        200: {
            'description': 'Роль успешно обновлена',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Роль не найдена',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        409: {
            'description': 'Роль с таким названием уже существует',
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
def update_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'status': False, 'message': 'Role not found'}), 404

    name = request.form.get('name')
    if name:
        existing_role = Role.query.filter_by(name=name).first()
        if existing_role:
            return jsonify({'status': False, 'message': 'Role with this name already exists'}), 409
        role.name = name

    db.session.commit()
    return jsonify({'status': True, 'message': 'Role updated successfully'})


@swag_from({
    'tags': ['Roles'],
    'parameters': [
        {
            'name': 'role_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID роли для удаления'
        }
    ],
    'responses': {
        200: {
            'description': 'Роль успешно удалена',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Роль не найдена',
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
def delete_role(role_id):
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'status': False, 'message': 'Role not found'}), 404

    db.session.delete(role)
    db.session.commit()
    return jsonify({'status': True, 'message': 'Role deleted successfully'})