from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.secret_key = "RickyDickyDooDahGrimes"
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SquadSync.db'

  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import Admin, Employee, Position

  create_database(app)

  return app

def create_database(app):
  if not path.exists('application/SquadSync.db'):
    with app.app_context():
        db.create_all()
        print("Created Datebase :)")
    