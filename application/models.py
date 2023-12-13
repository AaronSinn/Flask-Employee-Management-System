from . import db
from flask_login import UserMixin

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(35), nullable=False)
    lastName = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    positions = db.relationship('Position', backref='admin')
    employees = db.relationship('Employee', backref='admin')
    

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
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def to_dict(self):
        position = Position.query.filter_by(id=self.position_id).first()

        if position == None:
            return '', 400
        
        positionTitle = position.title
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
            'admin_id': self.admin_id
        }

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(175), nullable=False)
    basePay = db.Column(db.Integer)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    employees = db.relationship('Employee', backref='employee')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'basePay': self.basePay,
            'admin_id': self.admin_id
        }