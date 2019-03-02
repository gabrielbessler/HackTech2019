from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import *
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password_hash = Column(String(128))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Annotation(Base):
    __tablename__ = "annotations_table"
    id = Column(Integer, primary_key=True)
    sentence = Column(String(50))
    annotation = Column(String(50))
