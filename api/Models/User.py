from database import db
import bcrypt
from Models.UserRole import user_role
from Models.UserDepartment import user_department
from Models.Role import Role
from Models.Department import Department

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)  
    first_name = db.Column(db.String(50), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(500), unique=False)
    
    # Связи с ролями и отделами
    roles = db.relationship('Role', secondary=user_role, lazy='subquery', backref=db.backref('users', lazy=True))
    departments = db.relationship('Department', secondary=user_department, lazy='subquery', backref=db.backref('users', lazy=True))

    def __init__(self, login, first_name, last_name, password=None):  
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return '<User %r>' % self.login
