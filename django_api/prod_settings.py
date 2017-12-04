from settings import *


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
DATABASES['heroku'] = dj_database_url.config()
DATABASES['heroku']['CONN_MAX_AGE'] = 500