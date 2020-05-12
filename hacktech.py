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
from cloud import cloud
import wikipedia

app = Flask(__name__)
login = LoginManager(app)

init_db()

app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

entities = dict()
entity_keys = list()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

''' ======= DB HANDLER ======= ''' 

def _addAnnotation(sentence, annotation, user, prevSentence = None, nextSentence = None):
    a = Annotation(sentence, annotation, user, prevSentence, nextSentence)
    db_session.add(a)
    db_session.commit()

def _getAnnotations(sentence, prevSentence = None, nextSentence = None, userId = None):
    #if prevSentence and nextSentence:
    #    return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.prevSentence == prevSentence, Annotation.nextSentence == nextSentence)]
    #elif prevSentence:
    #    return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.prevSentence == prevSentence)]
    #elif nextSentence:
    #    return [a.__repr__() for a in Annotation.query.filter(Annotation.sentence == sentence, Annotation.nextSentence == nextSentence)]
    #else:
    if userId is None:
        L = [(a.__repr__(), false) for a in Annotation.query.filter(Annotation.sentence == sentence)]
    else: 
        L = [(a.__repr__(), a.checkuser(userId)) for a in Annotation.query.filter(Annotation.sentence == sentence)]

    print(L)
    if L is None:
        L = []
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


@app.route('/Depedantify')
def index():
    return render_template("index.html")

@app.route('/Depedantify/about')
def showAbout():
    return render_template('about.html')
    
@app.route('/Depedantify/register')
def displayRegistration():
    return render_template("register.html")

@app.route('/Depedantify/login')
def displayLogin():
    return render_template("login.html")

@app.route('/Depedantify/favorites')
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

@app.route('/Depedantify/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/Depedantify/register_attempt', methods=["POST"])
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

@app.route('/Depedantify/login_attempt', methods=["POST"])
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
    
@app.route('/Depedantify/img', methods=["POST"])
def getSimplifiedFromImage():
    '''
    Take image in the form of a JSON
    object, returns the simplfied text  
    '''
    result = request.get_json()
    
    requires = ["img"]
    if isValid(requires, result): 
        info = result["img"]
        if info[1:21] == "data:application/pdf":
            type = "PDF"
        else:
            type = "IMG"

        base64Image = info[info.find(',')+1:]


        text = 'undefined'

        if type == "PDF":
            text = OCR.process_PDF(base64Image)
        elif type == "IMG":
            text = OCR.process_IMG(base64Image)
       
        return text
    
    else:
        logging.info("Invalid request.")
        return "Failed to process image"

    return "OK"

@app.route('/Depedantify/text', methods=["POST"])
def getSimplifiedFromText():
    '''
    Take text in the form of a JSON 
    object, returns the simplified text
    '''
    result = request.get_json()
    requires = ["text"]
    offSetList = [] 

    if isValid(requires, result): 
        text = result['text']
        result = ""
        res = parse(text)
        lastOffSet = 0; 
        for sentence in res: 
            offSetList.append(lastOffSet)
            lastOffSet += len(sentence)

        isFavorite = False 
        article = Article.query.filter(Article.content == text).first()
        if current_user.is_authenticated and article is not None and article.id in current_user.getFavorites():
            isFavorite = True
        print(offSetList)
        return render_template("results.html", og=res, notOg=result, favorite=isFavorite, off = offSetList)
    else:
        logging.info("Invalid request: " + request + " at " + time.time()) 
        return "not a valid request"

@app.route('/Depedantify/word/<word_id>', methods=["POST"])
def getWordDef(word_id):
    app_id = '2e03965a'
    app_key = 'a64c8ad87dbcef0d9981af13ccc7957b'

    language = 'en'

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    r = r.json()["results"][0]["lexicalEntries"][0]['entries'][0]['senses'][0]['definitions']
    return json.dumps(r)

@app.route('/Depedantify/oPDF', methods=["POST"])
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
    

@app.route('/Depedantify/annotate', methods=["POST"])
def annotate():
    '''
    Adds annotation for a specific sentence
    '''
    results = request.get_json()
    requires = ["sentence", "annotation"]
    if isValid(requires, results) and current_user.is_authenticated:
        prevSentence = None if 'prevSentence' not in results else results['prevSentence']
        nextSentence = None if 'nextSentence' not in results else results['nextSentence']
        if results['sentence'] == None:
            return "Must be a sentence"
        if results['annotation'] == "":
            return "Cannot be empty"
       
        _addAnnotation(results['sentence'], results['annotation'], current_user.name, prevSentence, nextSentence)
        return "Annotation added"
    else:
        logging.info(f"Invalid request: {request} at {time.time()}")
        return "Not a valid annotation request"

@app.route('/Depedantify/check_favorite', methods=['POST'])
def checkFavorite():
    result = request.get_json()
    requires = ["text"]
    if isValid(requires, result):
        textToFavorite = result["text"]
    
        article = Article.query.filter(Article.content == textToFavorite).first()
        if article is None: 
            return "Not favorited"
        
        return article.id in current_user.getFavorites()

    return "Not a valid favorite check"

@app.route('/Depedantify/favorite', methods=['POST'])
def setFavorite():
    result = request.get_json()
    requires = ["text"]
    if isValid(requires, result):
        textToFavorite = result["text"]
                
        L = [x[1:-1] for x in textToFavorite[1:-1].split(", ")]
        textToFavorite = " ".join(L).strip()
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

@app.route('/Depedantify/unfavorite', methods=['POST'])
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
        if article is None: 
            return "Article was not favorited"

        current_user.remove_favorite(article.id)
        db_session.commit()
        return "Removed from favorites"

@app.route('/Depedantify/getAnnotations', methods=['POST'])
def getAnnotations():
    results = json.loads(request.data)
    requires = ["sentence"]
    if isValid(requires, results):
        if results["sentence"] is None:
            return "Not valid"
        prevSentence = None if 'prevSentence' not in results else results['prevSentence']
        nextSentence = None if 'nextSentence' not in results else results['nextSentence']
        if (current_user.is_authenticated):
            L = _getAnnotations(results['sentence'], prevSentence, nextSentence, current_user.id)
        else:
            L = _getAnnotations(results['sentence'], prevSentence, nextSentence, None)

        if L == []:
            return json.dumps([])

        return json.dumps(L[::-1])
    else:
        logging.info(f"Invalid request: {request} at {time.time()}")
        return "Not a valid getAnnotation request"

@app.route("/Depedantify/computeEntities", methods=['POST'])
def computeEntities():
    global entities
    global entity_keys

    results = json.loads(request.data)
    requires = ['text']
    if isValid(requires, results):

        text = results['text']

        resp = cloud.process_entities_response(cloud.get_entities(text))
        mappings = dict()
        for entry in resp:
            tag, occurences, link, _ = entry
            for occ in occurences:
                word = occ.text.content
                offset = 0
                try:
                    offset = occ.text.begin_offset
                except:
                    offset = 0
                mappings[(offset, word)] = (tag, link)
        keys = sorted(mappings.keys())
        entities = mappings
        entity_keys = keys
    
    print(entities)

    return "Done"

def binSearch(L, key, key_func):
    minInd = 0
    maxInd = len(L)
    midInd = 0
    while minInd < maxInd:
        midInd = (minInd + maxInd) // 2
        if key_func(L[midInd]) > key:
            maxInd = midInd
        elif key_func(L[midInd]) < key:
            minInd = midInd + 1
        else:
            return midInd
    return midInd

@app.route('/Depedantify/getEntities', methods=['POST'])
def getEntities():
    global entities
    global entity_keys


    results = json.loads(request.data)
    requires = ['sentence', 'position']
    annotations = list()
    if isValid(requires, results):
        sentence = results['sentence']
        position = int(results['position'])
        endPos   = position + len(sentence)
        firstEntry = binSearch
        curr = binSearch(entity_keys, position, lambda x: x[0])
        while curr < len(entity_keys) and entity_keys[curr][0] < endPos:
            _, word = entity_keys[curr]
            tag, link = entities[entity_keys[curr]]
            try:
                wikiSummary = wikipedia.summary(tag);
                annotations.append(f"<div> <div> {word} interpreted as {tag} with Wiki page {link}. </div> <div> {wikiSummary} </div> </div>")
            except:
                pass
            curr += 1
    
    s = "".join(annotations)
    print(s)
    return s


@app.route('/Depedantify/addRating', methods=['POST'])
def addRatingForAnnotation():
    results = json.loads(request.data)
    requires = ["score", "id"]
    print(results)

    if isValid(requires, results):
        if current_user.is_authenticated:
            
            annotation = Annotation.query.filter(Annotation.id == results["id"]).first()
            if annotation.checkuser(current_user.id):
                return "You already voted!"
            else:
                annotation.addRating(results["score"])
                annotation.addUser(current_user.id)
                db_session.commit()
                return "Updated score."
    
        return "You cannot vote without an account."
    
    else:
        print("Invalid")

    
    return "Invalid request."
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
    
