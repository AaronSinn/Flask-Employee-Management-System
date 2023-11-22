from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "RickyDickyDooDahGrimes"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adminInfo.db'
db = SQLAlchemy(app)

from app import views #advoid circular import