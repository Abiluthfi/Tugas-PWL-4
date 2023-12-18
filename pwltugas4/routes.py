
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('movies', '/movies')
    config.add_route('movie_detail', '/movies/{id}')
    config.scan('.views')
