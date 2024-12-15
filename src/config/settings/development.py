from .base import *  # noqa:F403

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }}


ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
# the URL prefix for serving static files during development.
STATIC_ROOT = BASE_DIR / "staticfiles"
# where static files should be collected when you run the collectstatic command. This is typically used in production.
