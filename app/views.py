from flask import render_template, url_for
from .forms import LoginForm, RegisterForm
from . import app



@app.route('/')
def home():

    return render_template('auth/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    return render_template('auth/register.html', form=form)
