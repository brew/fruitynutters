import os
import environ

import logging.config

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    INTERNAL_IPS=(tuple, ('127.0.0.1', )),
    ALLOWED_HOSTS=(tuple, ('localhost', )),
    DJANGO_LOGLEVEL=(str, 'INFO')
)

# Django settings for fruitynutters project.

SECRET_KEY = env('SECRET_KEY')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = env('DEBUG')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

INTERNAL_IPS = env('INTERNAL_IPS')

DATABASES = {
    'default': env.db(),
}

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATIC_ROOT = '/opt/services/djangoapp/static/'
MEDIA_ROOT = '/opt/services/djangoapp/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "www"),
]

# session age - one year
SESSION_COOKIE_AGE = 31536000

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'fruitynutters.notifications.notifications',
                'django.template.context_processors.media'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        },
        'DIRS': (
            os.path.join(os.path.dirname(__file__), 'templates'),
        )
    },
]

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fruitynutters.notifications.NotificationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

APPEND_SLASH = True

ROOT_URLCONF = 'fruitynutters.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'ganalytics',

    'fruitynutters.catalogue',
    'fruitynutters.cart',
)

GANALYTICS_TRACKING_CODE = env('GANALYTICS_TRACKING_CODE')

# Fruitynutters settings

ORDER_FORM_SEND_EMAIL = env('ORDER_FORM_SEND_EMAIL')
ORDER_FORM_REPLY_TO_EMAIL = env('ORDER_FORM_REPLY_TO_EMAIL')

# Logging Configuration

# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = env('DJANGO_LOGLEVEL')

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console',],
        },
    },
})
