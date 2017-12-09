from settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['CONN_MAX_AGE'] = 500
SECURE_SSL_REDIRECT = True
