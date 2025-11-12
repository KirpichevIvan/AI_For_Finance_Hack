from database import db

# Таблица связи между пользователями и отделами (many-to-many)
user_department = db.Table('user_department',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
)