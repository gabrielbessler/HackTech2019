import database
from hacktech import *
from database import db_session, init_db
from models import User, Annotation

while (True):
    r = input()
    if r == "":
        break
    else: 
        try:
            eval(r)
        except (TypeError, NameError) as e: 
            print(e)