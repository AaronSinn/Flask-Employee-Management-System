from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id='usernameInput')
    password = PasswordField('Password', validators=[DataRequired()], id='passwordInput')
    submit = SubmitField('Login')