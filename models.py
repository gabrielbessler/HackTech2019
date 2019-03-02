from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import *
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

USERNAME_LEN = 50
SENTENCE_LEN = 300
ANNOTATE_LEN = 1000

class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(USERNAME_LEN), unique=True)
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

    user = Column(String(USERNAME_LEN))
    rating = Column(BigInteger)
    ratingCount = Column(BigInteger)

    prevSentence = Column(String(SENTENCE_LEN))
    sentence = Column(String(SENTENCE_LEN))
    nextSentence = Column(String(SENTENCE_LEN))

    annotation = Column(String(ANNOTATE_LEN))

    def __init__(self, sentence, annotation, user, prevSentence = None, nextSentence = None):
        self.sentence = sentence
        self.annotation = annotation
        self.prevSentence = prevSentence
        self.nextSentence = nextSentence
        self.user = user
        self.rating = 0
        self.ratingCount = 0

    def __repr__(self):
        return f'<Annotation {self.id} {self.annotation} in {self.sentence} by {self.user} :-: {self.getRating()}>'

    def getRating(self):
        if not self.ratingCount:
            return "Unrated"
        return self.rating / self.ratingCount

    def addRating(self, rating):
        self.rating += rating
        self.ratingCount += 1