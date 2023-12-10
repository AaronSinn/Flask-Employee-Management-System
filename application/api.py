from flask import Blueprint, request, abort
from flask_login import login_required, current_user
from .models import Admin, Position
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
        return
    
    if request.method == 'DELETE':
        data = request.get_json()

        print(data)

        return '', 204