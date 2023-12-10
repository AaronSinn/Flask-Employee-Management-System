from flask import Blueprint, request, abort, flash
from flask_login import login_required, current_user
from .models import Admin, Position
from .forms import PositionForm
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
    
    if request.method == 'POST':
        data = request.get_json()
        print("DATA:", data)
        if 'id' not in data:
            abort(400)
        position = Position.query.get(data['id'])
        
        if 'title' in data:
            setattr(position, 'title', data['title'])

        if 'description' in data:
            setattr(position, 'description', data['description'])
        
        if 'basePay' in data:
            setattr(position, 'basePay', data['basePay'])

        db.session.commit()

        return '', 204
    
    if request.method == 'PUT':
        data = request.get_json()
        print(data)

        if data['title'].strip() == '' or data['description'].strip() == '' or data['basePay'] == '':
            return '', 404 #TODO: Put proper http code
        else:
            position = Position.query.filter_by(title=data['title']).first()
            print(position)
            if position:
                flash('Positon title already exists')
                return '', 406 #TODO: Put proper http code
            else:
                new_position = Position(title=data['title'], description=data['description'], basePay=data['basePay'], admin_id=current_user.id)
                db.session.add(new_position)
                db.session.commit()

                return '', 200
    if request.method == 'DELETE':
        data = request.get_json()

        print(data)

        return '', 204