import os


def gettext(s):
    return s


def _(x):
    return x


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DEBUG = True

ADMINS = [
    ("Marco", "marco@cruncher.ch"),
]

MANAGERS = ADMINS
LANGUAGES = [
    ("en", _("English")),
    ("de", _("German")),
    ("fr", _("French")),
    ("it", _("Italian")),
]


PARLER_LANGUAGES = {
    1: ({"code": "en"}, {"code": "de"}, {"code": "fr"}, {"code": "it"}),
    "default": {"fallback": "fr", "hide_untranslated": False},
}

PARLER_DEFAULT_LANGUAGE_CODE = "fr"


DEFAULT_LANGUAGE = 0

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "{{project_name}}",
    }
}


ALLOWED_HOSTS = [
    ".cruncher.ch",
    ".test.cruncher.ch",
    ".{{project_name}}.ch",
    "127.0.0.1",
    "0.0.0.0",
    "testserver",
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "KEY_PREFIX": "{{project_name}}",
    }
}

TIME_ZONE = "Europe/Zurich"
LANGUAGE_CODE = "en"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# INTERNAL_IPS = ('127.0.0.1', )
INTERNAL_IPS = []

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "tmp", "media")
STATIC_ROOT = os.path.join(BASE_DIR, "..", "tmp", "static")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"
DEV_STATIC_URLS = {}


STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

THUMBNAIL_DEFAULT_STORAGE = "easy_thumbnails.storage.ThumbnailFileSystemStorage"
THUMBNAIL_ALIASES = {
    "": {
        # "team-member": {"size": (1200, 900), "crop": True, "upscale": True},
    }
}


SECRET_KEY = "{{secret_key}}"
TEST_RUNNER = "django.test.runner.DiscoverRunner"


# TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR, 'templates'),
# )

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


ROOT_URLCONF = "{{project_name}}.urls"
AUTH_USER_MODEL = "users.User"


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "{{project_name}}.wsgi.application"


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
    "apps.users",
    "apps.cruncher",
    "apps.news",
    "parler",
    # Djano-cms
    "cms",
    "treebeard",
    "menus",
    "filer",
    "djangocms_snippet",
    "djangocms_text_ckeditor",
    "cmsplugin_filer_image",
    "cmsplugin_filer_file",
    # Common
    "sekizai",
    "gunicorn",
    "django_extensions",
    "impersonate",
    "easy_thumbnails",
    "storages",
    "django_otp",
    # https://django-otp-official.readthedocs.io/en/stable/overview.html#plugins-and-devices
    "django_otp.plugins.otp_totp",
    # "django_otp.plugins.otp_hotp",
    # "django_otp.plugins.otp_email",
    "django_otp.plugins.otp_static",
    # SMS: https://django-otp-twilio.readthedocs.io/en/latest/
    # Comms
    "django_check_seo",
    "meta",
    "scheduler",
)

FILER_CANONICAL_URL = "c/"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "apps.cruncher.auth_backends.EmailBackend",
)


IMPERSONATE = {
    "REDIRECT_URL": "/",
    "REQUIRE_SUPERUSER": True,
    "REDIRECT_FIELD_NAME": "next",
}
FILE_UPLOAD_PERMISSIONS = 0o644

BASE_URL = "https://{{project_name}}.cruncher.ch"


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        }
    },
}

# Default primary key field type to use for models that don’t have a field with primary_key=True.
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Set your DSN value
RAVEN_CONFIG = {"dsn": None}
RQ = {"DEFAULT_RESULT_TTL": 2678400}
SCHEDULER_QUEUES = {
    "default": {"HOST": "localhost", "PORT": 6379, "DB": 0, "DEFAULT_TIMEOUT": 360}
}

SHELL_PLUS = "ipython"

# Required for django-cms on 3.2
X_FRAME_OPTIONS = "SAMEORIGIN"
