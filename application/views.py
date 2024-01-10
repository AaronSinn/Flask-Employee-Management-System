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

    if admin:
        employees = Employee.query.filter_by(admin_id=admin.id).all()
        calendarEvents = CalendarDates.query.filter_by(admin_id=admin.id).all()
        departments = Department.query.filter_by(admin_id=admin.id).all()
        today = date.today()
        
        phoneNumbers = []#list of all the phone numbers
        birthdays = [] #list of all the birthdays
        totalEmployees = 0#total amount of employees and keeps count of iterations for phone numbers
        totalPayRole = 0
        largestDepartments = []#list to store the largest position(s)
        totalDepartments = 0
        employeesPerDepartment = 0

        for employee in employees:
            employeeBirthday = str(employee.birthday).split('-')
            brithdayMonth = int(employeeBirthday[1])
            brithdayDay = int(employeeBirthday[2])
            if brithdayMonth == today.month and brithdayDay == today.day:
                birthdays.append({
                    'name': employee.firstName + ' ' + employee.lastName,
                    'date': employee.birthday
                })
            #i only want to display 8 phone numbers
            if totalEmployees < 9:
                phoneNumbers.append({
                    'name': employee.firstName + ' ' + employee.lastName,
                    'phoneNumber': employee.phoneNumber
                })

            totalPayRole = totalPayRole + employee.salary
            totalEmployees += 1

        # randomDepartment = Department.query.filter_by(admin_id=admin.id).first()
        # if randomDepartment:
        #     max = randomDepartment.employeeCount #max is set to the employeeCount of a randomDepartment instead of 0. This way a department of 0 people wont be appended to the list and it will still work if all departments have 0 people                                    
        # else:
        #     max = 0
        max = 1
        for department in departments:       
            if department.employeeCount >= max:
                largestDepartments.append({
                    'title': department.title,
                    'employeeCount': department.employeeCount
                })
                max = department.employeeCount

            totalDepartments = totalDepartments + 1

        events = []
        for event in calendarEvents:
            startDateParsed = str(event.startDate).split('-')
            endDateParsed = str(event.endDate).split('-')
            startDate = date(year=int(startDateParsed[0]), month=int(startDateParsed[1]), day=int(startDateParsed[2]))
            endDate = date(year=int(endDateParsed[0]), month=int(endDateParsed[1]), day=int(endDateParsed[2]))

            startTimeParsed = str(event.startTime).split(':')
            endTimeParsed = str(event.endTime).split(':')

            if int(startTimeParsed[0]) > 12:
                startTime = str(int(startTimeParsed[0])-12) + ':' + startTimeParsed[1] + 'pm'
            elif int(startTimeParsed[0]) < 10:
                startTime = startTimeParsed[0][1] + ':' + startTimeParsed[1] + 'am'
            elif int(startTimeParsed[0]) == 11:
                startTime = startTimeParsed[0] + ':' + startTimeParsed[1] + 'am'
            else:
                startTime = startTimeParsed[0] + ':' + startTimeParsed[1] + 'pm'

            if int(endTimeParsed[0]) > 12:
                endTime = str(int(endTimeParsed[0])-12) + ':' + endTimeParsed[1] + 'pm'
            elif int(endTimeParsed[0]) < 10:
                endTime = endTimeParsed[0][1] + ':' + endTimeParsed[1] + 'am'
            elif int(endTimeParsed[0]) == 11:
                endTime = endTimeParsed[0] + ':' + endTimeParsed[1] + 'am'
            else: #endTimeParsed[0] == 12
                endTime = endTimeParsed[0] + ':' + endTimeParsed[1] + 'pm'

            if startDate <= today and endDate >= today:
                events.append({
                    'title': event.title,
                    'startDate': event.startDate,
                    'startTime': startTime,
                    'endDate': event.endDate,
                    'endTime': endTime
                })

        try:
            employeesPerDepartment = totalEmployees/totalDepartments
        except ZeroDivisionError:
            employeesPerDepartment = 0

        sideBarName=current_user.firstName + " " + current_user.lastName
        if len(sideBarName) > 16:
            sideBarName = '...'

        return render_template('dashboard.html', name=current_user.firstName + " " + current_user.lastName, sideBarName=sideBarName, events=events, birthdays=birthdays, username=current_user.username, 
                               phoneNumbers=phoneNumbers, totalEmployees=totalEmployees, totalPayRole=totalPayRole, largestDepartments=largestDepartments, employeesPerDepartment=employeesPerDepartment)
    else: #makes it so the user can't put a random string as a username in the URL. eg(http://127.0.0.1:5000/FakeUsername is not acceptable)
        return redirect(url_for('auth.login'))
    
@login_required
@views.route('/<username>/positions')
def positions(username):
    form = PositionForm()

    sideBarName=current_user.firstName + " " + current_user.lastName
    if len(sideBarName) > 16:
        sideBarName = '...'

    return render_template('positions.html', name=current_user.firstName + " " + current_user.lastName, sideBarName=sideBarName, username=username, form=form)

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

    sideBarName=current_user.firstName + " " + current_user.lastName
    if len(sideBarName) > 16:
        sideBarName = '...'

    return render_template('employees.html', name=current_user.firstName + " " + current_user.lastName, sideBarName=sideBarName, username=username, form=form)

@login_required
@views.route('/<username>/departments')
def departments(username):

    form = DepartmentForm()

    sideBarName=current_user.firstName + " " + current_user.lastName
    if len(sideBarName) > 16:
        sideBarName = '...'

    return render_template('departments.html', name=current_user.firstName + " " + current_user.lastName, sideBarName=sideBarName, username=username, form=form)

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

    sideBarName=current_user.firstName + " " + current_user.lastName
    if len(sideBarName) > 16:
        sideBarName = '...'

    return render_template('calendar.html', name=current_user.firstName + " " + current_user.lastName, sideBarName=sideBarName, username=username, form=form, editForm=editForm)


