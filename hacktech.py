import logging, time
from flask import Flask, render_template, request
import database
import json
import OCR 
from database import db_session, init_db
from models import User, Annotation
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)

init_db()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


''' ======= DB HANDLER ======= ''' 

def createUser(email, name, password):
    u = User(name, email)
    u.set_password(password) 
    db_session.commit()

def updatePw(username, password):
    pass 

def addAnnotation(self, sentence, annotation):
    a = Annotation()
    db_session.commit()

def getAnnotation(self, sentence):
    pass 



'''
i = annotationsTable.insert()
i.execute(
{
    'id': self.annotationCount,
    'sentence': sentence,
    'annotation': annotation,
}
)

self.annotationCount += 1

def getAnnotations(self, sentence):
selStmt = select([annotationsTable]).where(annotationsTable.c.sentence == sentence)
return [dict(result)['annotation'] for result in conn.execute(selStmt)]
'''

''' ======= DB HANDLER END ======= '''


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/login_request', methods=["POST"])
def login():
    pass

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def displayLoginScreen():
    return render_template("login.html")

@app.route('/img', methods=["POST"])
def getSimplifiedFromImage():
    '''
    Take image in the form of a JSON
    object, returns the simplfied text  
    '''
    result = request.get_json()
    

    if "img" in result: 
        info = result["img"]
        if info.startswith("data:application//pdf"):
            type = "PDF"
        else:
            type = "IMG"

        base64Image = info[24:]

        if type == "PDF":
            text = OCR.process_PDF(base64Image)
        elif type == "IMG":
            text = OCR.process_IMG(base64Image)
        
        print(text)
    else:
        print("nope")
        logging.info("Invalid request.")

    return "OK"

@app.route('/text', methods=["POST"])
def getSimplifiedFromText():
    '''
    Take text in the form of a JSON 
    object, returns the simplified text
    '''
    result = request.get_json()
    if 'text' in result: 
        text = result['text']
        return "hello world"
    else:
        logging.info("Invalid request: " + request + " at " + time.time()) 
        return "not a valid request"

@app.route('/annotate', methods=["POST"])
def annotate():
    '''
    Adds annotation for a specific sentence
    '''
    result = request.get_json()
    if 'sentence' in result and 'annotation' in result:
        database.addAnnotation(result['sentence'],result['annotation'])
    else:
        logging.info("Invalid request: " + request + " at " + time.time())

@app.route('/getAnnotaions', methods=['GET'])
def getAnnotations():
    return " temporary "

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
    