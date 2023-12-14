from flask import Blueprint, request, abort, flash
from flask_login import login_required, current_user
from datetime import datetime
from .models import Admin, Position, Employee
from .views import *
from . import db

api = Blueprint('api', __name__)

@api.route("/<username>/positions/data", methods=['GET', 'POST', 'PUT', 'DELETE'])
def data(username):
    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        positions = Position.query.filter_by(admin_id=admin.id)

        return {
            'data': [Position.to_dict() for Position in positions]
        }
    
    elif request.method == 'POST':
        data = request.get_json()
        print("POSITION DATA:", data)
        if 'id' not in data:
            abort(400)

        position = Position.query.filter_by(title=data['title']).first()

        if position:
            flash("Position already exists")
            return '', 400

        position = Position.query.get(data['id'])
        
        if 'title' in data:
            setattr(position, 'title', data['title'])

        if 'description' in data:
            setattr(position, 'description', data['description'])
        
        if 'basePay' in data:
            setattr(position, 'basePay', data['basePay'])

        db.session.commit()

        return '', 204
    
    elif request.method == 'PUT':
        data = request.get_json()
        print(data)

        if data['title'].strip() == '' or data['description'].strip() == '' or data['basePay'] == '':
            return '', 400
        else:
            position = Position.query.filter_by(title=data['title']).first()
            #print(position)
            if position:
                flash('Positon title already exists')
                return '', 400
            else:
                print('Data sent is good')
                new_position = Position(title=data['title'], description=data['description'], basePay=data['basePay'], admin_id=current_user.id)
                db.session.add(new_position)
                db.session.commit()
                print('Data commited')
                
                return '', 200
            
    elif request.method == 'DELETE':
        data = request.get_json()

        Position.query.filter_by(id=data['id']).delete()
        db.session.commit()

        return '', 204
    
@api.route('/<username>/employees/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def employees(username):

    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        employees = Employee.query.filter_by(admin_id=admin.id)

        return {
            'data': [Employee.to_dict() for Employee in employees]
        }
    
    elif request.method == 'POST':
        data = request.get_json()
        print("POSITION DATA:", data)
        if 'id' not in data:
            abort(400)

        
        return

    elif request.method == 'PUT':
        return 
    
    elif request.method == 'DELETE':
        data = request.get_json()

        Employee.query.filter_by(id=data['id']).delete()
        db.session.commit()

        return '', 204
