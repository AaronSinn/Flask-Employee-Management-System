from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
  app = Flask(__name__)
  app.secret_key = "RickyDickyDooDahGrimes"
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SquadSync.db'

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  return app

# db = SQLAlchemy(app)


# from app import views #advoid circular import