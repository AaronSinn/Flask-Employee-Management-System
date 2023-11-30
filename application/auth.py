from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Admin
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        print(form.username.data, form.password.data)
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if check_password_hash(admin.password, password):
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
        print(form.firstName.data, form.lastName.data, form.username.data, form.password.data)
        firstName = form.firstName.data
        lastName = form.lastName.data
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            flash("Username already taken.")
        else:
            new_admin = Admin(firstName=firstName, lastName=lastName, username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_admin)
            db.session.commit()

            return redirect(url_for('views.dashboard', username=username))

    print("Register form errors:", form.errors)
    return render_template('auth/register.html', form=form)
