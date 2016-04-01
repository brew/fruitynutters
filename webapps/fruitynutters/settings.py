import os
# Django settings for fruitynutters project.

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = (
    '127.0.0.1',
)


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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/fruitynutter/webapps/fruitynutters_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "www"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# session age - one year
SESSION_COOKIE_AGE = 31536000

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'fruitynutters.notifications.notifications',
    'django.core.context_processors.media',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fruitynutters.notifications.NotificationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

APPEND_SLASH = True

ROOT_URLCONF = 'fruitynutters.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

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

# GANALYTICS_TRACKING_CODE = 'UA-XXXXXXX-X'

# Fruitynutters settings

# ORDER_FORM_SEND_EMAIL = 'fruitynutters@example.com'
# ORDER_FORM_REPLY_TO_EMAIL = ORDER_FORM_SEND_EMAIL

try:
    from local_settings import *
except ImportError:
    pass
