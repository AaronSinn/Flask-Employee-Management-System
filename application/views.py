from flask import Blueprint, render_template, url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/<username>')
def dashboard(username):
    return render_template('dashboard.html')
