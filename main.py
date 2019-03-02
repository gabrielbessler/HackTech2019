from flask import Flask 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/img')
def getSimplifiedFromImage():
    '''
    Take image in the form of a JSON
    object, returns the simplfied text  
    '''
    pass 

@app.route('/text')
def getSimplifiedFromText():
    '''
    Take text in the form of a JSON 
    object, returns the simplified text
    '''
    pass 


