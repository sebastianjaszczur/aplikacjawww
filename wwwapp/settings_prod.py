from .settings_common import *

SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

DEBUG = False
ALLOWED_HOSTS = ['warsztatywww.pl']

# E-mail settings

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['GMAIL_ADDRESS']
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ['GMAIL_PASSWORD']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
        'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
        'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
    }
}

MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', ''), 'media')

GOOGLE_ANALYTICS_KEY = 'UA-12926426-8'
