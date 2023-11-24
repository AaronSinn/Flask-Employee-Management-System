from . import db
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase

class adminInfo(db.model, UserMixin):
    id = 