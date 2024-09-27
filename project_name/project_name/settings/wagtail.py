
import os


def gettext(s):
    return s


def _(x):
    return x


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


MIDDLEWARE = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "querycount.middleware.QueryCountMiddleware",
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
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
                "wagtail.contrib.settings.context_processors.settings",
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



WAGTAIL_SITE_NAME = "{{project_name}}"
#Add a WAGTAILDOCS_EXTENSIONS setting to specify the file types that Wagtail 
# will allow to be uploaded as documents. This can be omitted to allow all file types,
#  but this may present a security risk if untrusted users are allowed to
#  upload documents - see User Uploaded Files.

WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']
