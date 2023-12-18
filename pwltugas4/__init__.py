from pyramid.config import Configurator

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.views')
        tmdb_api_key = 'ae94bb10be51dc082a6f15cfb4376bd6'
        config.registry.settings['tmdb_api_key'] = tmdb_api_key

        config.scan()

    return config.make_wsgi_app()
