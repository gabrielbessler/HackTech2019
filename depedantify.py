import json
import re

transitions = dict()
with open('out.txt','r') as f:
    transitions = json.loads(f.read())

def _trans(word):
    if word in transitions:
        print("Yay!")
        return " ".join(transitions[word])
    return word

def simplify(text):
    sentence = re.findall(r"[\s]+|[\w]+|.", text)
    parsedSentence = [_trans(word) for word in sentence]
    return "".join(parsedSentence)
