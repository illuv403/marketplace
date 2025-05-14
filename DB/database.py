from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

"""
If executing on windows please set the URL of the database like that:
engine = create_engine("sqlite:///C:\\path\\to\\foo.DB")
A base class to initialise our database and create
Base from which all models will inherit.
"""
engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from DB.models import user, category, product, order
    Base.metadata.create_all(bind=engine)