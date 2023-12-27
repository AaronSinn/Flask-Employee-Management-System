from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired

from .models import Position
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id='usernameInput')
    password = PasswordField('Password', validators=[DataRequired()], id='passwordInput')
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('LOGIN')

class RegisterForm(FlaskForm):
    firstName = StringField('FirstName', validators=[DataRequired()], id='firstNameInput')
    lastName = StringField('LastName', validators=[DataRequired()], id='lastNameInput')
    username = StringField('Username', validators=[DataRequired()], id='usernameInput')
    password = PasswordField('Password', validators=[DataRequired()], id='passwordInput')
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class PositionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], id='titleInput')
    description = StringField('Description', validators=[DataRequired()], id='descriptionInput')
    basePay = IntegerField('Base Pay', validators=[DataRequired()], id='basePayInput')
    submit = SubmitField('Add Position')

class EmployeeForm(FlaskForm):

    firstName = StringField('FirstName', validators=[DataRequired()], id='firstNameInput')
    lastName = StringField('LastName', validators=[DataRequired()], id='lastNameInput')
    email = StringField('Email', validators=[DataRequired()], id='emailInput')
    phoneNumber = StringField('Phone Number', validators=[DataRequired()], id='phoneNumberInput')
    salary = IntegerField('Salary', validators=[DataRequired()], id='salaryInput')
    dateHired = DateField('Date Hired', validators=[DataRequired()], format='%Y-%m-%d', id='dateHiredInput')
    birthday = DateField('Date Hired', validators=[DataRequired()], format='%Y-%m-%d', id='birthdayInput')
    position = SelectField('Position', choices=[],validators=[DataRequired()], id='positionSelect')
    department = SelectField('Department', choices=[],validators=[DataRequired()], id='departmentSelect')
    submit = SubmitField('Add Employee')

class DepartmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], id='titleInput')
    description = StringField('Description', validators=[DataRequired()], id='descriptionInput')
    submit = SubmitField('Add Department')
