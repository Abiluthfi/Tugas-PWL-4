
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import bcrypt

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))

    def __init__(self, username, password):
        self.username = username
   
        self.password = bcrypt.using(salt="random").hash(password)

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)

    def __init__(self, title):
   
        if not title:
            raise ValueError("Title is required.")
        self.title = title

def init_db(engine, tmdb_api_key):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all()


   
    dummy_movies = [
        Movie(title="Inception"),
        Movie(title="The Shawshank Redemption"),
        Movie(title="The Godfather"),
        Movie(title="Pulp Fiction"),
        Movie(title="The Dark Knight"),
        Movie(title="Forrest Gump"),
        Movie(title="The Matrix"),
        Movie(title="Schindler's List"),
        Movie(title="Titanic"),
        Movie(title="Avatar"),
    ]
    DBSession.add_all(dummy_movies)

  
    config.registry.settings['tmdb_api_key'] = tmdb_api_key