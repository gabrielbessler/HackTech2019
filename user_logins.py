from werkzeug.security import generate_password_hash, check_password_hash 


def createAccount():
    hash = generate_password_hash(password)

def updatePassword():
    hash = generate_password_hash(password)

def checkLogin():
    check_password_hash(hash, password)