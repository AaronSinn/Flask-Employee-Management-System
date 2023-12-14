from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from datetime import datetime
from .forms import PositionForm, EmployeeForm
from .models import Admin, Position, Employee
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

    positions = Position.query.filter_by(admin_id=current_user.id)
    
    form = PositionForm()

    return render_template('positions.html', name=current_user.firstName + " " + current_user.lastName, username=username, form=form)

@login_required
@views.route('/<username>/employees')
def employees(username):

    # Obj1 = datetime(year=2020, month=5, day=23)
    # hireDate = Obj1.date() 
    # Obj2 = datetime(year=2003, month=7, day=13)
    # birthday = Obj2.date()

    # position = Position.query.filter_by(title='test').first()
    # if position:
    #     position_id = position.id

    # new_employee = Employee(firstName='Carl', lastName='Grimes', email='carl.grimes@me.com', phoneNumber='226-757-0160', salary=80000, dateHired=hireDate, birthday=birthday, position_id=position_id,admin_id=current_user.id)
    # db.session.add(new_employee)
    # db.session.commit()

    positions = Position.query.filter_by(admin_id=current_user.id).all()

    positionList = []
    for position in positions:
        positionList.append((position.id, position.title))

    # print("Position List:", positionList)

    form = EmployeeForm()
    form.position.choices = positionList

    return render_template('employees.html', name=current_user.firstName + " " + current_user.lastName, username=username, form=form)


