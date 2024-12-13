from .base import *  # noqa:F403

DEBUG = env('DEBUG')

AUTH_PASSWORD_VALIDATORS = []

DATABASES = {
    "default": env.db()
}

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
# the URL prefix for serving static files during development.
STATIC_ROOT = BASE_DIR / "staticfiles"
# where static files should be collected when you run the collectstatic command. This is typically used in production.
