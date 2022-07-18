from dataclasses import dataclass
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from employee_management import db, login_manager

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.Integer)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    manager = db.relationship('Employee', remote_side=[id])
    reportees = db.relationship('Employee', remote_side=[manager_id], uselist=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def is_admin(self):
        if self.role_id == 1:
            return True
        else:
            return False

    def __repr__(self):
        return f'<Employee: {self.first_name}>'


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


@dataclass
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return f'<Role: {self.name}>'
