from .settings_common import *

SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'

DEBUG = True
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE

ROOT_URLCONF = 'wwwapp.urls'

WSGI_APPLICATION = 'wwwapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, *MEDIA_URL.strip("/").split("/"))

GOOGLE_ANALYTICS_KEY = None