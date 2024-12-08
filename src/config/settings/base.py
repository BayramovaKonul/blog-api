
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_lt3)u+&2x%$n7*mkpt+u7c)qk-!0gal4jy!$dtw!*)44s#r4h'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_TZ = True

LANGUAGES = [ ('en', 'English'), ('az', 'Azerbaijan')]
LOCALE_PATHS = [BASE_DIR / 'locale', ]


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 'filters': {
    #     'request_id': {
    #         '()': 'log_request_id.filters.RequestIDFilter'
    #     }
    # },
    "formatters":{
        "json":{
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",   # json configuration
            "format": "{asctime} {levelname} {name} [%(request_id)s] {message} {filename} {funcName} {lineno}",
            "style": "{"
        }
    },
    "handlers":{
            "console":{
                "class": "logging.StreamHandler",
                "formatter": "json",
                # "filters": ["request_id"]
            },
            "file":{
                "class": "logging.FileHandler",
                "filename": "logs/general_logs.log",
                "formatter": "json",
                # "filters": ["request_id"]
            }
        },
    "loggers": {
        "general": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        },
        # "error_logger": {
        #     "level": "ERROR"
        # }
    }
}