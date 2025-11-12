from flask import jsonify, request
from Models.Department import Department, db
from flasgger import swag_from

@swag_from({
    'tags': ['Departments'],
    'responses': {
        200: {
            'description': 'Список отделов',
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
def get_departments():
    departments = Department.query.all()
    output = {
        'status': True if len(departments) > 0 else False,
        'message': "OK" if len(departments) > 0 else "Empty table",
        'data': []
    }
    for department in departments:
        department_data = {'id': department.id, 'name': department.name}
        output['data'].append(department_data)
    return jsonify(output)


@swag_from({
    'tags': ['Departments'],
    'parameters': [
        {
            'name': 'department_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID отдела'
        }
    ],
    'responses': {
        200: {
            'description': 'Информация об отделе',
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
            'description': 'Отдел не найден',
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
def get_department(department_id):
    department = Department.query.get(department_id)
    if department:
        department_data = {'id': department.id, 'name': department.name}
        return jsonify({'status': True, 'message': 'OK', 'data': department_data})
    else:
        return jsonify({'status': False, 'message': 'Department not found'}), 404


@swag_from({
    'tags': ['Departments'],
    'parameters': [
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Название отдела (должно быть уникальным)'
        }
    ],
    'responses': {
        201: {
            'description': 'Отдел успешно создан',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'department_id': {'type': 'integer'}
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
            'description': 'Отдел с таким названием уже существует',
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
def add_department():
    name = request.form.get('name')

    if not name:
        return jsonify({'status': False, 'message': 'Missing required field: name'}), 400

    existing_department = Department.query.filter_by(name=name).first()
    if existing_department:
        return jsonify({'status': False, 'message': 'Department with this name already exists'}), 409

    new_department = Department(name=name)
    db.session.add(new_department)
    db.session.commit()

    return jsonify({'status': True, 'message': 'Department added successfully', 'department_id': new_department.id}), 201


@swag_from({
    'tags': ['Departments'],
    'parameters': [
        {
            'name': 'department_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID отдела для обновления'
        },
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Новое название отдела'
        }
    ],
    'responses': {
        200: {
            'description': 'Отдел успешно обновлен',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Отдел не найден',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        409: {
            'description': 'Отдел с таким названием уже существует',
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
def update_department(department_id):
    department = Department.query.get(department_id)
    if not department:
        return jsonify({'status': False, 'message': 'Department not found'}), 404

    name = request.form.get('name')
    if name:
        existing_department = Department.query.filter_by(name=name).first()
        if existing_department:
            return jsonify({'status': False, 'message': 'Department with this name already exists'}), 409
        department.name = name

    db.session.commit()
    return jsonify({'status': True, 'message': 'Department updated successfully'})


@swag_from({
    'tags': ['Departments'],
    'parameters': [
        {
            'name': 'department_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID отдела для удаления'
        }
    ],
    'responses': {
        200: {
            'description': 'Отдел успешно удален',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Отдел не найден',
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
def delete_department(department_id):
    department = Department.query.get(department_id)
    if not department:
        return jsonify({'status': False, 'message': 'Department not found'}), 404

    db.session.delete(department)
    db.session.commit()
    return jsonify({'status': True, 'message': 'Department deleted successfully'})