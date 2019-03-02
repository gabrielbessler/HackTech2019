from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session

database_url = "sqlite:///server.db"
engine = create_engine(database_url, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import User, Annotation
    Base.metadata.create_all(bind=engine)
