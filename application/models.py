from . import db
from flask_login import UserMixin
from sqlalchemy.types import Time

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(35), nullable=False)
    lastName = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    positions = db.relationship('Position', backref='admin')
    employees = db.relationship('Employee', backref='admin')
    departments = db.relationship('Department', backref='admin')
    calendarDates = db.relationship('CalendarDates', backref='admin')
    
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(35), nullable=False)
    lastName = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phoneNumber = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.Float, nullable=False) 
    dateHired = db.Column(db.Date, nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def to_dict(self):
        position = Position.query.filter_by(id=self.position_id).first()
        try:
            positionTitle = position.title
        except: #if the position was deleted
            positionTitle = 'None'

        department = Department.query.filter_by(id=self.department_id).first()
        try:
            departmentTitle = department.title
        except: #if the department was deleted
            departmentTitle = 'None'

        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'phoneNumber': self.phoneNumber,
            'salary': self.salary,
            'dateHired': str(self.dateHired),
            'birthday': str(self.birthday),
            'position': positionTitle,
            'department': departmentTitle,
            'admin_id': self.admin_id
        }

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(175), nullable=False)
    basePay = db.Column(db.Integer)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    employees = db.relationship('Employee', backref='position')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'basePay': self.basePay,
            'admin_id': self.admin_id
        }
    
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(175), nullable=False)
    employeeCount = db.Column(db.Integer, default=0)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    employees = db.relationship('Employee', backref='department')

    def to_dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'employeeCount': self.employeeCount,
            'admint_id': self.admin_id
        }
    
class CalendarDates(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    startDate = db.Column(db.Date, nullable=True)
    startTime = db.Column(Time, nullable=True)
    endDate = db.Column(db.Date, nullable=False)
    endTime = db.Column(Time, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def to_dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'startDate': self.startDate,
            'startTime': self.startTime,
            'endDate': self.endDate,
            'endTime': self.endTime,
            'frequency': self.frequency,
            'admint_id': self.admin_id
        }
