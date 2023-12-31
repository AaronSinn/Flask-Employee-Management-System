from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from datetime import datetime, time, date
from .forms import PositionForm, EmployeeForm, DepartmentForm, EventForm, EventFormEdit
from .models import Admin, Position, Employee, Department, CalendarDates
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@login_required #user must be logged in to access the dashboard
@views.route('/<username>')
def dashboard(username):

    admin = Admin.query.filter_by(username=username).first()
    employees = Employee.query.filter_by(admin_id=admin.id).all()
    calendarEvents = CalendarDates.query.filter_by(admin_id=admin.id).all()
    today = date.today()

    brithdays = [] #list of all the birthdays
    for employee in employees:
        if str(employee.brithday) == str(today):
            brithdays.append({
                'name': employee.name,
                'date': employee.brithday
            })
    
    events = []
    for event in calendarEvents:
        startDateParsed = str(event.startDate).split('-')
        endDateParsed = str(event.endDate).split('-')
        startDate = date(year=startDateParsed[0], month=startDateParsed[1], day=startDateParsed[2])
        endDate = date(year=endDateParsed[0], month=endDateParsed[1], day=endDateParsed[2])

        if startDate <= today and endDate >= today:
            events.append({
                'title': event.title,
                'startDate': event.startDate,
                'startTime': event.startTime,
                'endDate': event.endDate,
                'endTime': event.endTime
            })


    if admin:
        return render_template('dashboard.html', name=current_user.firstName + " " + current_user.lastName)
    else: #makes it so the user can't put a random string as a username in the URL. eg(http://127.0.0.1:5000/FakeUsername is not acceptable)
        return redirect(url_for('auth.login'))
    
@login_required
@views.route('/<username>/positions')
def positions(username):
    form = PositionForm()

    return render_template('positions.html', name=current_user.firstName + " " + current_user.lastName, username=username, form=form)

@login_required
@views.route('/<username>/employees')
def employees(username):

    positions = Position.query.filter_by(admin_id=current_user.id).all()
    positionList = []
    for position in positions:
        positionList.append((position.id, position.title))

    departments = Department.query.filter_by(admin_id=current_user.id).all()
    departmentList = []
    for department in departments:
        departmentList.append((department.id, department.title))
    
    form = EmployeeForm()
    form.department.choices = departmentList
    form.position.choices = positionList

    return render_template('employees.html', name=current_user.firstName + " " + current_user.lastName, username=username, form=form)

@login_required
@views.route('/<username>/departments')
def departments(username):

    form = DepartmentForm()

    return render_template('departments.html', name=current_user.firstName + " " + current_user.lastName, username=username, form=form)

@login_required
@views.route('<username>/calendar')
def calendar(username):

    # startDateParsed ='2023-12-03'.split('-')
    # endDateParsed ='2024-12-04'.split('-')
    # startDate = datetime(year=int(startDateParsed[0]), month=int(startDateParsed[1]), day=int(startDateParsed[2])).date()
    # endDate = datetime(year=int(endDateParsed[0]), month=int(endDateParsed[1]), day=int(endDateParsed[2])).date()

    # startTime = time(hour=9, minute=21)
    # endTime = time(hour=14, minute=2)


    # new_event = CalendarDates(title='test3', startDate=startDate, startTime=startTime, endDate=endDate, endTime=endTime, frequency=1, admin_id=current_user.id)
    # db.session.add(new_event)
    # db.session.commit()

    form = EventForm()
    editForm = EventFormEdit()
    return render_template('calendar.html', name=current_user.firstName + " " + current_user.lastName, username=username, form=form, editForm=editForm)


