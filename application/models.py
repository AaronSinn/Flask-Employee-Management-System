from . import db
from flask_login import UserMixin

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(35), nullable=False)
    lastName = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(35), nullable=False)
    lastName = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    dateHired = db.Column(db.DateTime, nullable=False)
    birthday = db.Column(db.DateTime)
    position = db.relationship('Position', uselist=False)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(175), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))