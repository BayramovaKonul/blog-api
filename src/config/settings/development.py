from .base import *

DEBUG=True

AUTH_PASSWORD_VALIDATORS = [

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ["*"]

STATIC_URL = '/static/'
# the URL prefix for serving static files during development.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# where static files should be collected when you run the collectstatic command. This is typically used in production.