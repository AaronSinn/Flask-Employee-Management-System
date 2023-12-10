from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from .forms import PositionForm
from .models import Admin, Position
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@login_required #user must be logged in to access the dashboard
@views.route('/<username>')
def dashboard(username):

    admin = Admin.query.filter_by(username=username).first()
    if admin:
        return render_template('dashboard.html', name=current_user.firstName + " " + current_user.lastName)
    else: #makes it so the user can't put a random string as a username in the URL. eg(http://127.0.0.1:5000/FakeUsername is not acceptable)
        return redirect(url_for('auth.login'))
    
@login_required
@views.route('/<username>/positions')
def positions(username):
    admin = current_user.id
 
    # new_positions = Position(title="Doctor", description="Patch up wounds.", basePay=80000, admin_id=admin)
    # db.session.add(new_positions)

    # new_positions = Position(title="Runner", description="Get supplies.",  basePay=65000, admin_id=admin)
    # db.session.add(new_positions)
    # db.session.commit()

    # new_positions = Position(title="Doctor", description="Get me bit.", basePay=0, admin_id=admin)
    # db.session.add(new_positions)

    # new_positions = Position(title="Shane", description="Catch Frogs.",  basePay=65000, admin_id=admin)
    # db.session.add(new_positions)
    # db.session.commit()


    positions = Position.query.filter_by(admin_id=current_user.id)
    
    form = PositionForm()

    return render_template('positions.html', name=current_user.firstName + " " + current_user.lastName, positions=positions, username=username, form=form)

# @login_required
# @views.route('/<username>/positions/edit')
# def editPositions(username):
#     return render_template('edit.html')

