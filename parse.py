from collections import defaultdict

KnownSentences = defaultdict(set)

sentenceDelims = ".!?"

def splitDelim(text, delim):
    parts = [part.strip() for part in text.split(delim)]
    return [part + (delim if i+1<len(parts) else "") for i,part in enumerate(parts)]

def parse(text):
    text = text.strip()
    sentences = [text]
    for delim in sentenceDelims:
        sentences = sum([splitDelim(sentence,delim) for sentence in sentences if sentence],[])
    return [s.strip() for s in sentences]

def annotate(sentence, annotation):
    KnownSentences[sentence].add(annotation)

def getAnnotations(sentence):
    return "\n".join(KnownSentences[sentence])

def printParagraph(sentences):
    for sentence in sentences:
        print("-"*20 + "\n" + sentence + "\n")
        if sentence in KnownSentences:
            print("\n->".join(KnownSentences[sentence]))
