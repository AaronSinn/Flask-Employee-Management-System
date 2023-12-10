from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Admin
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if current_user.is_authenticated: #if the user is already signed in they can skip the login page
        return redirect(url_for('views.dashboard', username=current_user.username))

    if form.validate_on_submit():
        print(form.username.data, form.password.data)
        username = form.username.data
        password = form.password.data
        rememberMe = form.rememberMe.data

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if check_password_hash(admin.password, password):
                login_user(admin, remember=rememberMe)
                return redirect(url_for('views.dashboard', username=username))
            else:
                print("Incorrect password.")
                flash("Incorrect password.", category='passwordError')
        else:
            print("Username not found.")
            flash("Username not found.",category='usernameError')
    
    print("Login form errors:", form.errors)
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # print(form.firstName.data, form.lastName.data, form.username.data, form.password.data)
        firstName = form.firstName.data
        lastName = form.lastName.data
        username = form.username.data
        password = form.password.data
        rememberMe = form.rememberMe.data

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            flash("Username already taken.")
        else:
            new_admin = Admin(firstName=firstName, lastName=lastName, username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin,remember=rememberMe)
            return redirect(url_for('views.dashboard', username=username))

    print("Register form errors:", form.errors)
    return render_template('auth/register.html', form=form)

@auth.route("/logout")
@login_required #user must be logged in to access this route
def logout():
    name=str(current_user.firstName + " " + current_user.lastName)
    logout_user()
    return render_template('auth/logout.html', name=name)