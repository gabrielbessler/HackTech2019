from collections import defaultdict
import database

# annon = database.Annotations()

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

def _annotate(sentence, annotation):
    annon.addAnnotation(sentence, annotation)

def _getAnnotations(sentence):
    return "\n".join(annon.getAnnotations(sentence))

def _printParagraph(sentences):
    for sentence in sentences:
        print("-"*20 + "\n" + sentence + "\n")
        print(getAnnotations(sentence))

if __name__ == '__main__':
    _annotate("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "Bad sentence do not reccomend")
    _annotate("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "Best sentence ever!!!")
    _annotate("Vivamus nec elit eu ex auctor sodales vel quis ex.", "This sentence confused me...")
    _sentences = parse("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin efficitur nisi a bibendum maximus. Quisque varius placerat ex, nec feugiat ex vulputate id. Sed et velit in eros faucibus sagittis in quis enim. Donec aliquet nec enim eget pellentesque. Integer et dignissim elit. Vivamus ac tempor orci. Aliquam erat volutpat. Ut et justo vel leo blandit tincidunt. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Phasellus ultrices tristique pellentesque. Vivamus nec elit eu ex auctor sodales vel quis ex. Fusce vitae orci quis nunc sollicitudin sagittis a id nulla. Etiam id dolor vel elit ultricies imperdiet eu ut nisl. Sed mattis eget nisi eu porta. ")
    _printParagraph(sentences)
