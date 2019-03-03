import logging, time
from flask import Flask, render_template, request, redirect, url_for
import database
import json
import OCR 
from database import db_session, init_db
from models import User, Annotation
from flask_login import LoginManager, current_user, login_user, logout_user
from sqlalchemy import *
from parse import *
import requests

app = Flask(__name__)
login = LoginManager(app)

init_db()

app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

''' ======= DB HANDLER ======= ''' 

def _addAnnotation(sentence, annotation, user, prevSentence = None, nextSentence = None):
    a = Annotation(sentence, annotation, user, prevSentence, nextSentence)
    db_session.add(a)
    db_session.commit()

def _getAnnotations(sentence, prevSentence = None, nextSentence = None):
    if prevSentence and nextSentence:
        return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.prevSentence == prevSentence, Annotation.nextSentence == nextSentence)]
    elif prevSentence:
        return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.prevSentence == prevSentence)]
    elif nextSentence:
        return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.nextSentence == nextSentence)]
    else:
        return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence)]

def _addRating(annotationID, rating):
    Annotation.query.filter(Annotation.id == annotationID).first().addRating(rating)

''' ======= DB HANDLER END ======= '''

def isValid(requirements, request):
    if not request:
        return False
    for req in requirements:
        if req not in request:
            return False
    return True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def showAbout():
    return render_template('about.html')
    
@app.route('/register')
def displayRegistration():
    return render_template("register.html")

@app.route('/login')
def displayLogin():
    return render_template("login.html")

@app.route('/favorites')
def get_favories():
    if not current_user.is_authenticated:
        return redirect(url_for("displayLogin"))

    favorites = current_user.getFavorites()
    return render_template("favorites.html", favs=favorites)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register_attempt', methods=["POST"])
def register_attempt():
    result = request.get_json()
    if "pass" in result and "email" in result:
        pw = result["pass"]
        email = result["email"]
        usrname = result["name"]

        result = list(User.query.filter(or_(User.email == email, User.name == usrname)))
        if len(result) == 0:
            u = User(usrname, email)
            u.set_password(pw) 
            db_session.add(u)
            db_session.commit()
            return "Succeed"
        else: 
            return "Username and email must be unique."
    
    return "Could not process request"

@app.route('/login_attempt', methods=["POST"])
def login_attempt():
    if current_user.is_authenticated:
        return ""
    
    result = request.get_json()

    username = result["name"]
    pw = result["pass"]

    user = User.query.filter(User.name == username).first()

    if user is None or not user.check_password(pw):
        print("incorrect")
        return "Invalid username or password"
    else:
        login_user(user)
        print("good job")
        return "Succeed"
    
@app.route('/img', methods=["POST"])
def getSimplifiedFromImage():
    '''
    Take image in the form of a JSON
    object, returns the simplfied text  
    '''
    result = request.get_json()
    
    print('begin')

    requires = ["img"]
    if isValid(requires, result): 
        info = result["img"]
        if info[1:21] == "data:application/pdf":
            type = "PDF"
        else:
            type = "IMG"

        base64Image = info[info.find(',')+1:]

        print('processing')

        text = 'undefined'

        if type == "PDF":
            text = OCR.process_PDF(base64Image)
        elif type == "IMG":
            text = OCR.process_IMG(base64Image)
       
        print('done')
        print(len(text))
        return text[0]
    else:
        logging.info("Invalid request.")
        return "Failed to process image"

    return "OK"

@app.route('/text', methods=["POST"])
def getSimplifiedFromText():
    '''
    Take text in the form of a JSON 
    object, returns the simplified text
    '''
    result = request.get_json()
    requires = ["text"]

    if isValid(requires, result): 
        text = result['text']
        result = "Wow this text is so simple"
        return render_template("results.html", og=parse(text), notOg=result)
    else:
        logging.info("Invalid request: " + request + " at " + time.time()) 
        return "not a valid request"

@app.route('/word/<word_id>', methods=["POST"])
def getWordDef(word_id):
    app_id = '2e03965a'
    app_key = 'a64c8ad87dbcef0d9981af13ccc7957b'

    language = 'en'

    print("hello")

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    r = r.json()["results"][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions']
    return json.dumps(r)

@app.route('/toPDF', methods=["POST"])
def toPDF():
    result = request.get_json()
    
    requires = ["img"]
    if isValid(requires, result): 
        info = result["img"]
        if info[1:21] == "data:application/pdf":
            type = "PDF"
        else:
            type = "IMG"

    if type == "PDF":
        return OCR.PDFFromBase64(info[info.find(',')+1:])
    elif type == "IMG":
        return OCR.PDFFromBase64(info[info.find(',')+1:])
    

@app.route('/annotate', methods=["POST"])
def annotate():
    '''
    Adds annotation for a specific sentence
    '''
    results = request.get_json()
    requires = ["sentence", "annotation"]
    if isValid(requires, results) and current_user.is_authenticated:
        prevSentence = None if 'prevSentence' not in results else results['prevSentence']
        nextSentence = None if 'nextSentence' not in results else results['nextSentence']
        _addAnnotation(results['sentence'], results['annotation'], current_user.name, prevSentence, nextSentence)
        return "Annotation added"
    else:
        logging.info(f"Invalid request: {request} at {time.time()}")
        return "Not a valid annotation request"

@app.route('/getAnnotations', methods=['POST'])
def getAnnotations():
    results = json.loads(request.data)
    requires = ["sentence"]
    if isValid(requires, results):
        prevSentence = None if 'prevSentence' not in results else results['prevSentence']
        nextSentence = None if 'nextSentence' not in results else results['nextSentence']
        return json.dumps(_getAnnotations(results['sentence'], prevSentence, nextSentence))
    else:
        logging.info(f"Invalid request: {request} at {time.time()}")
        return "Not a valud getAnnotation request"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
    
