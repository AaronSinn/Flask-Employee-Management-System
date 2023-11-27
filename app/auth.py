from flask import Blueprint, render_template
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        print(form.username.data, form.password.data)

        return render_template('base.html')
    print("Login form errors:", form.errors)

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(form.firstName.data, form.lastName.data, form.username.data, form.password.data)
    
    print("Register form errors:", form.errors)

    return render_template('auth/register.html', form=form)
