from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from tableDef import *

class Annotations:
    def __init__(self):
        self.engine = create_engine("sqlite:///server.db", echo=False)
        metadata.bind = self.engine

        self.annotationCount = 0

        # Build annotations table
        if not self.engine.dialect.has_table(self.engine, "annotations_table"):
            annotationsTable.create(self.engine)
        else:
            conn = self.engine.connect()
            self.annotationCount = conn.execute('SELECT COUNT(*) FROM annotations_table').scalar()

    def addAnnotation(self, sentence, annotation):
        conn = self.engine.connect()
        
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
        conn = self.engine.connect()
        selStmt = select([annotationsTable]).where(annotationsTable.c.sentence == sentence)
        return [dict(result)['annotation'] for result in conn.execute(selStmt)]

