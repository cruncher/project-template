# -*- coding: utf-8 -*-
import os

gettext = lambda s: s
_ = lambda x: x
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Marco', 'marco@cruncher.ch')
)

MANAGERS = ADMINS
LANGUAGES = [
    ('en', _('English')),
    ('de', _('German')),
    ('fr', _('French')),
    ('it', _('Italian')),
]

DEFAULT_LANGUAGE = 0

# create user {{project_name}} with password '{{project_name}}';
# create database {{project_name}} with encoding='UTF-8' owner={{project_name}};
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '{{project_name}}',                      # Or path to database file if using sqlite3.
    }
}

ALLOWED_HOSTS = ['.cruncher.ch', '.test.cruncher.ch', '.{{project_name}}.ch']

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, '{{project_name}}.db'),
    }
}
"""


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': '{{project_name}}'
    }
}

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'en'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

INTERNAL_IPS = ('127.0.0.1', )

MEDIA_ROOT = os.path.join(PROJECT_DIR, '..', '..', 'tmp', 'media')
STATIC_ROOT = os.path.join(PROJECT_DIR, '..', '..', 'tmp', 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, '..', 'static'),
    # os.path.join(PROJECT_DIR, '..', '..', 'res'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter', ]

SECRET_KEY = '{{ secret_key }}'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    # 'utils.contextprocessors.conf'
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, '..', 'templates'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, '..', 'locale'),
)


ROOT_URLCONF = '{{project_name}}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{project_name}}.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'apps.styleguide',

    'sekizai',
    'compressor',
    'gunicorn',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'crispy_forms',
    'front',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


FILE_UPLOAD_PERMISSIONS = 0644

ADMIN_KEYBOARD_SHORTCUTS_HIDE_ICON = True

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': None
}


try:
    from settings_local import *  # NOQA
except ImportError:
    pass

try:
    INSTALLED_APPS = INSTALLED_APPS + ADDITIONAL_INSTALLED_APPS
except:
    pass
