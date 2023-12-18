# scripts/initialize_db.py
from pyramid.paster import get_appsettings, setup_logging
from pwltugas4.models import init_db
from sqlalchemy import engine_from_config

def main():
    setup_logging('development.ini')
    settings = get_appsettings('development.ini')
    engine = engine_from_config(settings, 'sqlalchemy.')
    init_db(engine)

if __name__ == '__main__':
    main()
