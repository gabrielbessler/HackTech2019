import logging, time
from flask import Flask, render_template, request, redirect, url_for
import database
import json
import OCR 
from database import db_session, init_db
from models import User, Annotation, Article
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
    #if prevSentence and nextSentence:
    #    return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.prevSentence == prevSentence, Annotation.nextSentence == nextSentence)]
    #elif prevSentence:
    #    return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.prevSentence == prevSentence)]
    #elif nextSentence:
    #    return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.nextSentence == nextSentence)]
    #else:
    L = [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence)]
    print(L)
    return L

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
def get_favorites():
    if not current_user.is_authenticated:
        return redirect(url_for("displayLogin"))

    favorites = current_user.getFavorites()
    
    favorites = [Article.query.filter(Article.id == x).first().content for x in favorites if x and x != ""]
    L = []
    for favorite in favorites:
        if len(favorite) == 0:
            continue
        print(favorite)
        if favorite[0] == "[" and favorite[-1] == "]":
            guy = [x[1:-1] for x in favorite[1:-1].split(", ")]
            dude = " ".join(guy).strip()
            L.append(dude)
        else:
            L.append(favorite)

    return render_template("favorites.html", favs=L)

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
        return "Invalid username or password"
    else:
        login_user(user)
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
        result = ""
        res = parse(text)
        isFavorite = False 
        print(text)
        article = Article.query.filter(Article.content == text).first()
        print(article)
        if current_user.is_authenticated and article is not None and article.id in current_user.getFavorites():
            isFavorite = True 
            print("yep")
        return render_template("results.html", og=res, notOg=result, favorite=isFavorite)
    else:
        logging.info("Invalid request: " + request + " at " + time.time()) 
        return "not a valid request"

@app.route('/word/<word_id>', methods=["POST"])
def getWordDef(word_id):
    app_id = '2e03965a'
    app_key = 'a64c8ad87dbcef0d9981af13ccc7957b'

    language = 'en'

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

@app.route('/check_favorite', methods=['POST'])
def checkFavorite():
    result = request.get_json()
    requires = ["text"]
    if isValid(requires, result):
        textToFavorite = result["text"]
    
        print(textToFavorite)

        article = Article.query.filter(Article.content == textToFavorite).first()
        if article is None: 
            return "Not favorited"
        
        return article.id in current_user.getFavorites()

    return "Not a valid favorite check"

@app.route('/favorite', methods=['POST'])
def setFavorite():
    result = request.get_json()
    requires = ["text"]
    if isValid(requires, result):
        textToFavorite = result["text"]
                
        L = [x[1:-1] for x in textToFavorite[1:-1].split(", ")]
        textToFavorite = " ".join(L).strip()
        print("text: " + textToFavorite)
        # Check if the article already exists 
        article = Article.query.filter(Article.content == textToFavorite).first()
        if article is None: 
            a = Article(textToFavorite)
            db_session.add(a)
            
            if a.id not in current_user.getFavorites():
                current_user.add_favorite(a.id)
                       
            db_session.commit()
        else: 
            if article.id in current_user.getFavorites():
                return "Already favorited!"
            current_user.add_favorite(article.id)
            db_session.commit()

        return "Favorited."

    return "Not a falid favorite request"

@app.route('/unfavorite', methods=['POST'])
def unsetFavorite():
    result = request.get_json()
    requires = ["text"]
    if isValid(requires, result):
        textToFavorite = result["text"]
        L = [x[1:-1] for x in textToFavorite[1:-1].split(", ")]
        textToFavorite = " ".join(L).strip()

        # Can only favorite if you are logged in 
        if not current_user.is_authenticated:
            return "Must be logged in"
        
        # Get the article ID 
        article = Article.query.filter(Article.content == textToFavorite).first()
        print(article.id)
        if article is None: 
            return "Article was not favorited"

        current_user.remove_favorite(article.id)
        db_session.commit()
        return "Removed from favorites"

@app.route('/getAnnotations', methods=['POST'])
def getAnnotations():
    results = json.loads(request.data)
    print(results)
    requires = ["sentence"]
    if isValid(requires, results):
        if results["sentence"] is None:
            return "Not a valid request"
        prevSentence = None if 'prevSentence' not in results else results['prevSentence']
        nextSentence = None if 'nextSentence' not in results else results['nextSentence']
        L = _getAnnotations(results['sentence'], prevSentence, nextSentence)
        print(L)
        if L == []:
            return json.dumps([])

        return json.dumps(L[::-1])
    else:
        logging.info(f"Invalid request: {request} at {time.time()}")
        return "Not a valid getAnnotation request"

@app.route('/addRating', methods=['POST'])
def addRatingForAnnotation():
    
    results = json.loads(request.data)
    requires = ["score", "id"]
    
    if isValid(requires, results):
        if current_user.is_authenticated:
            annotation = Annotation.query.filter(Annotation.id == results["id"]).first()
            if annotation.checkuser(current_user.id):
                return "You already voted!"
            else:
                annotation.addRating(results["score"])
                annotation.addUser(current_user.id)
                return "Updated score."
    
        return "You cannot vote without an account."
    
    db_session.commit()
    return "Invalid request."
    
    pass
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
    
