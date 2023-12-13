from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

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
    submit = SubmitField('Add position')

class EmployeeForm(FlaskForm):
    firstName = StringField('FirstName', validators=[DataRequired()], id='firstNameInput')
    lastName = StringField('LastName', validators=[DataRequired()], id='lastNameInput')
    