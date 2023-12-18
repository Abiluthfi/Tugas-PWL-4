# tests/test_views.py
from pyramid import testing
from pwltugas4.models import init_db, DBSession, User
from passlib.hash import bcrypt

def test_register_view():
    with testing.testConfig() as config:
        init_db(config.registry.settings['tmdb_api_key'])
        config.include('.views')
        app = config.make_wsgi_app()

        request = testing.DummyRequest(json_body={'username': 'testuser', 'password': 'testpass'})
        response = app.handle_request(request)

        assert response.status_code == 200
        assert response.json_body == {'message': 'Registration successful'}

def test_login_view():
    # Simpan pengguna ke basis data
    user = User(username='testuser', password=bcrypt.using(salt="random").hash("testpass"))
    DBSession.add(user)

    with testing.testConfig() as config:
        config.include('.views')
        app = config.make_wsgi_app()

        request = testing.DummyRequest(json_body={'username': 'testuser', 'password': 'testpass'})
        response = app.handle_request(request)

        assert response.status_code == 200
        assert 'token' in response.json_body
