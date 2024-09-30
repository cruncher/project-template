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

{%- if cookiecutter.use_parler == 'y' %}
PARLER_LANGUAGES = {
    1: ({"code": "en"}, {"code": "de"}, {"code": "fr"}, {"code": "it"}),
    "default": {"fallback": "fr", "hide_untranslated": False},
}

PARLER_DEFAULT_LANGUAGE_CODE = "fr"
{%- endif %}


DEFAULT_LANGUAGE = 0

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "{{cookiecutter.project_slug}}",
    }
}


ALLOWED_HOSTS = [
    ".cruncher.ch",
    ".test.cruncher.ch",
    ".{{cookiecutter.project_slug}}.ch",
    "127.0.0.1",
    "0.0.0.0",
    "testserver",
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "KEY_PREFIX": "{{cookiecutter.project_slug}}",
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


SECRET_KEY = "unsecure-secret-key"
TEST_RUNNER = "django.test.runner.DiscoverRunner"


# TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR, 'templates'),
# )

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


ROOT_URLCONF = "{{cookiecutter.project_slug}}.urls"
AUTH_USER_MODEL = "users.User"


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "{{cookiecutter.project_slug}}.wsgi.application"


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
    #"apps.news",
    "apps.home",
    "apps.search",
    {%- if cookiecutter.use_parler %}
    "parler",
    {%- endif %}

    # Djano-cms
    # "cms",
    # "treebeard",
    # "menus",
    # "filer",
    # "djangocms_snippet",
    # "djangocms_versioning",
    # "djangocms_text_ckeditor",
    # "cmsplugin_filer_image",
    # "cmsplugin_filer_file",
    {%- if cookiecutter.cms == "Wagtail" %}
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'modelcluster',
    'taggit',
    {% elif cookiecutter.cms == "DjangoCMS" %}
    "cms",
    "treebeard",
    "menus",
    "filer",
    "djangocms_snippet",
    "djangocms_versioning",
    "djangocms_text_ckeditor",
    "cmsplugin_filer_image",
    "cmsplugin_filer_file",
    "django_check_seo",
    "meta",
    {%- endif %}

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
    "scheduler",
)

{%- if cookiecutter.cms == "DjangoCMS" %}
CMS_PAGE_CACHE = True
CMS_PLACEHOLDER_CACHE = True
CMS_PLUGIN_CACHE = True

CMS_CACHE_DURATIONS = {"content": 60, "menus": 3600, "permissions": 3600}


CMS_TEMPLATES = (("cms/home.html", "Page template"),)
CMS_CONFIRM_VERSION4 = True

# CMS_PLACEHOLDER_CONF = {
#     'background image': {
#         'plugins': ['BackgroundImagePlugin'],
#         'limits': {
#             'global': 1
#         }
#     }
# }

META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "{{cookiecutter.project_slug}}.ch"
META_USE_OG_PROPERTIES = True
META_SITE_TYPE = "website"

PAGE_META_DESCRIPTION_LENGTH = 160


# DEFAULTS
DJANGO_CHECK_SEO_SETTINGS = {
    "content_words_number": [300, 600],
    "internal_links": 1,
    "external_links": 1,
    "meta_title_length": [30, 60],
    "meta_description_length": [50, PAGE_META_DESCRIPTION_LENGTH],
    "keywords_in_first_words": 50,
    "max_link_depth": 4,
    "max_url_length": 70,
}


{% elif cookiecutter.cms == "Wagtail" %}
# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

WAGTAIL_SITE_NAME = "{{ cookiecutter.project_name }}"
#Add a WAGTAILDOCS_EXTENSIONS setting to specify the file types that Wagtail 
# will allow to be uploaded as documents. This can be omitted to allow all file types,
#  but this may present a security risk if untrusted users are allowed to
#  upload documents - see User Uploaded Files.

WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']
{%- endif %}

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)
INTERNAL_IPS = []

MIDDLEWARE = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "cms.middleware.utils.ApphookReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    {%- if cookiecutter.cms == "DjangoCMS" %}
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    {% elif cookiecutter.cms == "Wagtail" %}
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    {%- endif %}
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "querycount.middleware.QueryCountMiddleware",


    # 'django.middleware.cache.FetchFromCacheMiddleware',
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "..", "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.debug",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                {%- if cookiecutter.cms == "DjangoCMS" %}
                "cms.context_processors.cms_settings",
                {% elif cookiecutter.cms == "Wagtail" %}
                "wagtail.contrib.settings.context_processors.settings",
                {%- endif %}
            ],
            "debug": False,
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    }
]

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

BASE_URL = "https://{{cookiecutter.domain_name}}"


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.


def suppress_allowed_hosts(record):
    from django.core.exceptions import SuspiciousOperation, DisallowedHost

    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
        if isinstance(exc_value, DisallowedHost):
            return False
    return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "suppress_allowed_hosts": {
            "()": "django.utils.log.CallbackFilter",
            "callback": suppress_allowed_hosts,
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false", "suppress_allowed_hosts"],
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


{% if cookiecutter.cms == "DjangoCMS" %}
# Required for django-cms on 3.2
X_FRAME_OPTIONS = "SAMEORIGIN"
{%- endif %}
