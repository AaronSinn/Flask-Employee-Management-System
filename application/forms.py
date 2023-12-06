from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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
