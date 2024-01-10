from flask import Blueprint, request, abort, flash
from flask_login import login_required, current_user
from datetime import datetime, time
import phonenumbers
from .models import Admin, Position, Employee, Department, CalendarDates
from .views import *
from . import db

import re

api = Blueprint('api', __name__)

#Positions page API
@api.route("/<username>/positions/data", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def data(username):
    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        positions = Position.query.filter_by(admin_id=admin.id)

        return {
            'data': [Position.to_dict() for Position in positions]
        }
    
    elif request.method == 'PATCH':
        data = request.get_json()
        print("POSITION DATA:", data)
        if 'id' not in data:
            abort(400)

        if 'title' in data:
            position = Position.query.filter_by(title=data.get('title')).first()
            if position:
                flash("Position already exists")
                return '', 400

        position = Position.query.get(data.get('id'))
        
        if 'title' in data:
            setattr(position, 'title', data.get('title'))

        elif 'description' in data:
            setattr(position, 'description', data.get('description'))
        
        elif 'basePay' in data:
            setattr(position, 'basePay', int(data.get('basePay')[1:]))

        db.session.commit()

        return '', 200
    
    elif request.method == 'POST':
        data = request.get_json()
        print(data)

        if data['title'].strip() == '' or data.get('description').strip() == '' or data.get('basePay') == '':
            return '', 400
        else:
            position = Position.query.filter_by(title=data.get('title')).first()
            if position:
                flash('Positon title already exists')
                return '', 400
            else:
                new_position = Position(title=data.get('title'), description=data.get('description'), basePay=data.get('basePay'), admin_id=current_user.id)
                db.session.add(new_position)
                db.session.commit()
                
                return '', 200
            
    elif request.method == 'DELETE':
        data = request.get_json()

        Position.query.filter_by(id=data.get('id')).delete()
        db.session.commit()

        return '', 204

#Employee Page API 
@api.route('/<username>/employees/data', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def employees(username):

    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        employees = Employee.query.filter_by(admin_id=admin.id)

        return {
            'data': [Employee.to_dict() for Employee in employees]
        }
    
    if request.method == 'PATCH':
        data = request.get_json()
        print(data)
        if 'id' not in data:
            abort(400)

        employee = Employee.query.get(data.get('id'))

        if 'firstName' in data:
            setattr(employee, 'firstName', data.get('firstName'))
        elif 'lastName' in data:
            setattr(employee, 'lastName', data.get('lastName'))
        
        elif 'position' in data:
            try: #checks to see if the position exists
                position = Position.query.filter_by(title = data.get('position')).first()
                position_id = position.id
            except AttributeError as e: #returns 400 if the position does not exist
                print("PUT position error:", e)
                return '', 400

            setattr(employee, 'position_id', position_id)

        elif 'department' in data:
            try: #checks to see if the department exists
                department = Department.query.filter_by(title = data.get('department')).first()
                department_id = department.id
            except AttributeError as e: #returns 400 if the department does not exist
                print("PUT department error:", e)
                return '', 400

            #updates the employee count for the department the employee was removed from
            oldDepartment = Department.query.filter_by(title = data.get('previousValue')).first()
            if oldDepartment:
                newEmployeeCount = oldDepartment.employeeCount - 1
                setattr(oldDepartment, 'employeeCount', newEmployeeCount)

            #updates the new information
            newEmployeeCount = department.employeeCount + 1
            setattr(department, 'employeeCount', newEmployeeCount)
            setattr(employee, 'department_id', department_id)

        elif 'email' in data:
            setattr(employee, 'email', data.get('email'))
        
        elif 'phoneNumber' in data:
            phoneNumber = phonenumbers.format_number(phonenumbers.parse(data['phoneNumber'], 'CA'), phonenumbers.PhoneNumberFormat.NATIONAL)
            setattr(employee, 'phoneNumber', phoneNumber)
        
        elif 'salary' in data:
            setattr(employee, 'salary', int(data.get('salary')[1:]))
        
        elif 'dateHired' in data:
            pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if pattern.match(data.get('dateHired')):
                dateHiredParsed = data.get('dateHired').split('-')
                dateHired = datetime(year=int(dateHiredParsed[0]), month=int(dateHiredParsed[1]), day=int(dateHiredParsed[2]))
                setattr(employee, 'dateHired', dateHired.date())
            else:
                return '', 400
        
        elif 'birthday' in data:
            pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if pattern.match(data.get('birthday')):
                brithdayParsed = data.get('birthday').split('-')
                birthday = datetime(year=int(brithdayParsed[0]), month=int(brithdayParsed[1]), day=int(brithdayParsed[2]))
                setattr(employee, 'birthday', birthday.date())
            else:
                return '', 400
        
        db.session.commit()
        return '', 200

    if request.method == 'POST':
        data = request.get_json()

        #returns 400 for invalid input
        # if data.get('firstName').strip() == "" or data.get('lastName').strip() == "" or data.get('email').strip() == "" or data.get('phoneNumber').strip() == "":
        #     print('Invalid Input for employee POST request')
        #     return '', 400
        
        phoneNumber = phonenumbers.format_number(phonenumbers.parse(data.get('phoneNumber'), 'CA'), phonenumbers.PhoneNumberFormat.NATIONAL)
        dateHiredParsed = data.get('dateHired').split('-')
        brithdayParsed = data.get('birthday').split('-')
        dateHired = datetime(year=int(dateHiredParsed[0]), month=int(dateHiredParsed[1]), day=int(dateHiredParsed[2]))
        birthday = datetime(year=int(brithdayParsed[0]), month=int(brithdayParsed[1]), day=int(brithdayParsed[2]))

        new_employee = Employee(firstName=data.get('firstName'), lastName=data.get('lastName'), email=data.get('email'), phoneNumber=phoneNumber, salary=data.get('salary'), 
                                dateHired=dateHired.date(), birthday=birthday.date(), position_id=data.get('position'), department_id = data.get('department'), admin_id=current_user.id)
       
        db.session.add(new_employee)

        #updates the employee count for the department
        department = Department.query.filter_by(id=data.get('department')).first()
        newEmployeeCount = department.employeeCount + 1
        setattr(department, 'employeeCount', newEmployeeCount)

        db.session.commit()
        return '', 200
    
    if request.method == 'DELETE':
        data = request.get_json()

        Employee.query.filter_by(id=data.get('id')).delete()

        #updates the employee count for the department
        print(data)
        department = Department.query.filter_by(title=data.get('department')).first()
        if department:
            newEmployeeCount = department.employeeCount - 1
            setattr(department, 'employeeCount', newEmployeeCount)

        db.session.commit()
        return '', 200

#Department Page API
@api.route('/<username>/departments/data', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def departments(username):

    #GET
    if request.method == 'GET':
        admin = Admin.query.filter_by(username=username).first()
        departments = Department.query.filter_by(admin_id = admin.id)
        
        return {
            'data': [Department.to_dict() for Department in departments]
        }, 200
    
    if request.method == 'PATCH':
        data = request.get_json()
        print(data)
        if 'id' not in data:
            abort(400)

        department = Department.query.filter_by(id=data.get('id')).first()

        if 'title' in data:
            setattr(department, 'title', data.get('title'))
        
        if 'description' in data:
            setattr(department, 'description', data.get('description'))

        db.session.commit()

        return '', 200

    if request.method == 'POST':
        data = request.get_json()

        #checks if the department already exists
        department = Department.query.filter_by(title=data.get('title'))
        if department:
            return '', 400

        new_department = Department(title=data.get('title'), description=data.get('description'), admin_id=current_user.id)
        db.session.add(new_department)
        db.session.commit()

        return '', 200
    
    if request.method == 'DELETE':
        data = request.get_json()
        
        #removes employee from the department getting deleted
        employeesInDepartment = Employee.query.filter_by(department_id = data.get('id')).all()
        for employee in employeesInDepartment:
            employee.department_id = None

        Department.query.filter_by(id=data.get('id')).delete() 

        db.session.commit()
        return '', 200

@api.route('<username>/calendar/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def events(username):
    #GET
    if request.method == 'GET':

        admin = Admin.query.filter_by(username=username).first()
        employees = Employee.query.filter_by(admin_id=admin.id)
        calendarDates = CalendarDates.query.filter_by(admin_id=admin.id)
        events = []

        #adds the employees brithdays to the event list
        for employee in employees:
            events.append({
                'title': employee.firstName + "'s" + " brithday",
                #makes the brithdays repeat annually until 2999-12-31
                'rrule': {
                    'freq': 'yearly',
                    'dtstart': str(employee.birthday),
                    'until': '2999-12-31'
                }
            })
        
        for event in calendarDates:

            #if the event has a frequency that repeats 
            frequency=None
            if  event.frequency != 0:

                if event.frequency == 1:
                    frequency='weekly'
                elif event.frequency == 2:
                    frequency='monthly'
                elif event.frequency == 3:
                    frequency='yearly'

                events.append({
                    'id': event.id,
                    'title': event.title,
                    'timeZone': 'America/Toronto',
                    'rrule':{
                        'freq': frequency,
                        'dtstart': str(event.startDate) + 'T' + str(event.startTime),
                        'until': str(event.endDate) + 'T' + str(event.endTime),
                    }
                })

            else:#if the event does not repeat
                events.append({
                    'id': event.id,
                    'title': event.title,
                    'timeZone': 'America/Toronto',
                    'start': str(event.startDate) + 'T' + str(event.startTime),
                    'end': str(event.endDate) + 'T' + str(event.endTime),
                })


        return {'events': events}

    #POST
    if request.method == 'POST':
        data = request.get_json()
        admin = Admin.query.filter_by(username=username).first()

        startDateParsed = data.get('startDate').split('-')
        endDateParsed = data.get('endDate').split('-')
        startDate = datetime(year=int(startDateParsed[0]), month=int(startDateParsed[1]), day=int(startDateParsed[2]))
        endDate = datetime(year=int(endDateParsed[0]), month=int(endDateParsed[1]), day=int(endDateParsed[2]))

        startTimeParsed = data.get('startTime').split(':')
        endTimeParsed = data.get('endTime').split(':')
        startTime = time(hour=int(startTimeParsed[0]), minute=int(startTimeParsed[1]))
        endTime = time(hour=int(endTimeParsed[0]), minute=int(endTimeParsed[1]))

        new_event = CalendarDates(title=data.get('title'), startDate=startDate, startTime=startTime, endDate=endDate, endTime=endTime, frequency=data.get('frequency'), admin_id=admin.id)
        db.session.add(new_event)
        db.session.commit()

        return '', 200
    
    if request.method == 'PUT':
        data = request.get_json()
        admin = Admin.query.filter_by(username=username).first()
        event = CalendarDates.query.filter_by(id=data.get('id')).first()

        startDateParsed = data.get('startDate').split('-')
        endDateParsed = data.get('endDate').split('-')
        startDate = datetime(year=int(startDateParsed[0]), month=int(startDateParsed[1]), day=int(startDateParsed[2]))
        endDate = datetime(year=int(endDateParsed[0]), month=int(endDateParsed[1]), day=int(endDateParsed[2]))

        startTimeParsed = data.get('startTime').split(':')
        endTimeParsed = data.get('endTime').split(':')
        startTime = time(hour=int(startTimeParsed[0]), minute=int(startTimeParsed[1]))
        endTime = time(hour=int(endTimeParsed[0]), minute=int(endTimeParsed[1]))

        if 'title' in data:
            setattr(event, 'title', data.get('title'))
        
        if 'startDate' in data:
            setattr(event, 'startDate', startDate)
        
        if 'startTime' in data:
            setattr(event, 'startTime', startTime)

        if 'endDate' in data:
            setattr(event, 'endDate', endDate)
        
        if 'endTime' in data:
            setattr(event, 'endTime', endTime)
        
        if 'frequency' in data:
            setattr(event, 'frequency', data.get('frequency'))
        
        db.session.commit()

        return '', 200

    if request.method == 'DELETE':
        data = request.get_json()
        print(data)
        event = CalendarDates.query.filter_by(id=data.get('id')).delete()

        db.session.commit()

        return '', 200

        


    
