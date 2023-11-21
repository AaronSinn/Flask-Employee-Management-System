from flask import render_template, url_for
from app.forms import LoginForm, RegisterForm
from app import app


@app.route('/')
def home():

    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm()

    return render_template('register.html', form=form)
