import dj_database_url
import os

import settings


settings.SECRET_KEY = os.environ.get('SECRET_KEY')
settings.DEBUG = False
settings.DATABASES['heroku'] = dj_database_url.config()
settings.DATABASES['heroku']['CONN_MAX_AGE'] = 500