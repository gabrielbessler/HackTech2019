import logging, time
from flask import Flask, render_template, request
import database
import json
import OCR 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/img', methods=["POST"])
def getSimplifiedFromImage():
    '''
    Take image in the form of a JSON
    object, returns the simplfied text  
    '''
    result = request.get_json()
    if "img" in result: 
        base64Image = result["img"][24:][:50]
        text = OCR.process(base64Image)
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

