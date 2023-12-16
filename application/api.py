from flask import Blueprint, request, abort, flash
from flask_login import login_required, current_user
from datetime import datetime
import phonenumbers
from .models import Admin, Position, Employee
from .views import *
from . import db

import re

api = Blueprint('api', __name__)

@api.route("/<username>/positions/data", methods=['GET', 'POST', 'PUT', 'DELETE'])
def data(username):
    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        positions = Position.query.filter_by(admin_id=admin.id)

        return {
            'data': [Position.to_dict() for Position in positions]
        }
    
    elif request.method == 'PUT':
        data = request.get_json()
        print("POSITION DATA:", data)
        if 'id' not in data:
            abort(400)

        if 'title' in data:
            position = Position.query.filter_by(title=data['title']).first()
            if position:
                flash("Position already exists")
                return '', 400

        position = Position.query.get(data['id'])
        
        if 'title' in data:
            setattr(position, 'title', data['title'])

        elif 'description' in data:
            setattr(position, 'description', data['description'])
        
        elif 'basePay' in data:
            setattr(position, 'basePay', data['basePay'])

        db.session.commit()

        return '', 200
    
    elif request.method == 'POST':
        data = request.get_json()
        print(data)

        if data['title'].strip() == '' or data['description'].strip() == '' or data['basePay'] == '':
            return '', 400
        else:
            position = Position.query.filter_by(title=data['title']).first()
            if position:
                flash('Positon title already exists')
                return '', 400
            else:
                new_position = Position(title=data['title'], description=data['description'], basePay=data['basePay'], admin_id=current_user.id)
                db.session.add(new_position)
                db.session.commit()
                
                return '', 200
            
    elif request.method == 'DELETE':
        data = request.get_json()

        Position.query.filter_by(id=data['id']).delete()
        db.session.commit()

        return '', 204

#Employee Page API 
@api.route('/<username>/employees/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def employees(username):

    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        employees = Employee.query.filter_by(admin_id=admin.id)

        return {
            'data': [Employee.to_dict() for Employee in employees]
        }
    
    elif request.method == 'PUT':
        data = request.get_json()
        print(data)
        if 'id' not in data:
            abort(400)

        employee = Employee.query.get(data['id'])

        if 'firstName' in data:
            setattr(employee, 'firstName', data['firstName'])

        elif 'lastName' in data:
            setattr(employee, 'lastName', data['lastName'])
        
        elif 'position' in data:
            try: #checks to see if the position exists
                position = Position.query.filter_by(title = data['position']).first()
                position_id = position.id
            except AttributeError as e: #returns 400 if the position does not exist
                print("PUT position error:", e)
                return '', 400

            setattr(employee, 'position_id', position_id)

        elif 'email' in data:
            setattr(employee, 'email', data['email'])
        
        elif 'phoneNumber' in data:
            phoneNumber = phonenumbers.format_number(phonenumbers.parse(data['phoneNumber'], 'CA'), phonenumbers.PhoneNumberFormat.NATIONAL)
            setattr(employee, 'phoneNumber', phoneNumber)
        
        elif 'salary' in data:
            setattr(employee, 'salary', data['salary'])
        
        elif 'dateHired' in data:
            pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if pattern.match(data['dateHired']):
                dateHiredParsed = data['dateHired'].split('-')
                dateHired = datetime(year=int(dateHiredParsed[0]), month=int(dateHiredParsed[1]), day=int(dateHiredParsed[2]))
                setattr(employee, 'dateHired', dateHired.date())
            else:
                return '', 400
        
        elif 'birthday' in data:
            pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if pattern.match(data['birthday']):
                brithdayParsed = data['birthday'].split('-')
                birthday = datetime(year=int(brithdayParsed[0]), month=int(brithdayParsed[1]), day=int(brithdayParsed[2]))
                setattr(employee, 'birthday', birthday.date())
            else:
                return '', 400
        
        db.session.commit()
        return '', 200

    elif request.method == 'POST':
        data = request.get_json()

        #returns 400 for invalid input
        if data['firstName'].strip() == "" or data['lastName'].strip() == "" or data['email'].strip() == "" or data['phoneNumber'].strip() == "":
            print('Invalid Input for employee POST request')
            return '', 400
        
        phoneNumber = phonenumbers.format_number(phonenumbers.parse(data['phoneNumber'], 'CA'), phonenumbers.PhoneNumberFormat.NATIONAL)
        dateHiredParsed = data['dateHired'].split('-')
        brithdayParsed = data['birthday'].split('-')
        dateHired = datetime(year=int(dateHiredParsed[0]), month=int(dateHiredParsed[1]), day=int(dateHiredParsed[2]))
        birthday = datetime(year=int(brithdayParsed[0]), month=int(brithdayParsed[1]), day=int(brithdayParsed[2]))

        new_employee = Employee(firstName=data['firstName'], lastName=data['lastName'], email=data['email'], phoneNumber=phoneNumber, salary=data['salary'], 
                                dateHired=dateHired.date(), birthday=birthday.date(), position_id=data['position'], admin_id=current_user.id)
       
        db.session.add(new_employee)
        db.session.commit()
        return '', 200
    
    elif request.method == 'DELETE':
        data = request.get_json()

        Employee.query.filter_by(id=data['id']).delete()
        db.session.commit()
        return '', 200
