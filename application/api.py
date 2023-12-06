from flask import Blueprint, request
from flask_login import login_required, current_user
from .models import Admin, Position
from . import db

api = Blueprint('api', __name__)

@api.route("/<username>/positions/data", methods=['GET', 'POST'])
def data(username):
    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        positions = Position.query.filter_by(admin_id=admin.id)

        return {
            'data': [Position.to_dict() for Position in positions]
        }
    
    if request.method == 'POST':
        