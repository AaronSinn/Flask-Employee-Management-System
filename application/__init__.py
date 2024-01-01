from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.secret_key = "ThisIsAFakeSecrectKeyThatShouldBeUniqueAndKnownToNobody:)"
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SquadSync.db'

  db.init_app(app)

  from .views import views
  from .auth import auth
  from .api import api

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(api, url_prefix='/')

  from .models import Admin, Employee, Position

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login' 
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_admin(id):
     return Admin.query.get(int(id))

  return app

def create_database(app):
  if not path.exists('application/SquadSync.db'):
    with app.app_context():
        db.create_all()
        print("Created Datebase :)")
    