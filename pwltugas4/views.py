import jwt
from pyramid.view import view_config
from pyramid.response import Response
from .models import DBSession, User, Movie
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from passlib.hash import bcrypt
from .security import RootACL
import datetime
import requests

TMDB_API_KEY = 'ae94bb10be51dc082a6f15cfb4376bd6'

@view_config(route_name='register', renderer='json', request_method='POST')
def register(request):
    data = request.json_body
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return HTTPBadRequest("Username and password are required.")

    hashed_password = bcrypt.using(salt="random").hash(password)

    user = User(username=username, password=hashed_password)
    DBSession.add(user)

    return {'message': 'Registration successful'}

@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    data = request.json_body
    username = data.get('username')
    password = data.get('password')

    user = DBSession.query(User).filter_by(username=username).first()

    if user and bcrypt.verify(password, user.password):
        jwt_token = jwt.encode({'sub': user.id}, 'abi.120140151', algorithm='HS256')
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        return {'token': jwt_token, 'exp': exp_time.timestamp()}
    else:
        return HTTPBadRequest("Invalid username or password.")

@view_config(route_name='movies', renderer='json', request_method='GET', permission='view')
def get_movies(request):
    tmdb_url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}'
    try:
        response = requests.get(tmdb_url)
        response.raise_for_status()

        tmdb_data = response.json()
        movies = tmdb_data.get('results', [])
        formatted_movies = [{'id': movie['id'], 'title': movie['title']} for movie in movies]

        return formatted_movies 
    except requests.exceptions.RequestException as e:
        return HTTPBadRequest(f"Failed to fetch movies from TMDB. Error: {str(e)}")

@view_config(route_name='movies', renderer='json', request_method='POST', permission='edit')
def create_movie(request):
    data = request.json_body
    title = data.get('title')

    if not title:
        return HTTPBadRequest("Title is required.")

    tmdb_url = f'https://api.themoviedb.org/3/movie?api_key={TMDB_API_KEY}'

    try:
        payload = {'title': title}
        response = requests.post(tmdb_url, json=payload)
        response.raise_for_status()

        return {'message': 'Movie created successfully'}
    except requests.exceptions.RequestException as e:
        return HTTPBadRequest(f"Failed to create movie on TMDB. Error: {str(e)}")

@view_config(route_name='movies/{id}', renderer='json', request_method='GET', permission='view')
def get_movie(request):
    movie_id = request.matchdict.get('id')
    movie = DBSession.query(Movie).filter_by(id=movie_id).first()

    if not movie:
        return HTTPNotFound(f"Movie with ID {movie_id} not found.")

    return {'id': movie.id, 'title': movie.title}

@view_config(route_name='movies/{id}', renderer='json', request_method='PUT', permission='edit')
def update_movie(request):
    movie_id = request.matchdict.get('id')
    movie = DBSession.query(Movie).filter_by(id=movie_id).first()

    if not movie:
        return HTTPNotFound(f"Movie with ID {movie_id} not found.")

    data = request.json_body
    title = data.get('title')

    if not title:
        return HTTPBadRequest("Title is required.")

    movie.title = title

    return {'message': 'Movie updated successfully'}

@view_config(route_name='movies/{id}', renderer='json', request_method='DELETE', permission='edit')
def delete_movie(request):
    movie_id = request.matchdict.get('id')
    movie = DBSession.query(Movie).filter_by(id=movie_id).first()

    if not movie:
        return HTTPNotFound(f"Movie with ID {movie_id} not found.")

    DBSession.delete(movie)

    return {'message': 'Movie deleted successfully'}
