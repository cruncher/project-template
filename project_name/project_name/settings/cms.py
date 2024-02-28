import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

gettext = lambda s: s

CMS_PAGE_CACHE = True
CMS_PLACEHOLDER_CACHE = True
CMS_PLUGIN_CACHE = True

CMS_CACHE_DURATIONS = {"content": 60, "menus": 3600, "permissions": 3600}


# CMS_PLACEHOLDER_CONF = {
#     'background image': {
#         'plugins': ['BackgroundImagePlugin'],
#         'limits': {
#             'global': 1
#         }
#     }
# }

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
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
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
                "cms.context_processors.cms_settings",
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

CMS_TEMPLATES = (("cms/home.html", "Page template"),)
CMS_CONFIRM_VERSION4 = True

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)
# # https://github.com/divio/djangocms-text-ckeditor#configuration
# CMS_EDITOR_STYLE_SET = [
#     {'name': 'Titre 0 (300px)', 'element': 'h1', 'attributes': {'class': 'text-00'}},
#     {'name': 'Titre 1 (150px)', 'element': 'h1', 'attributes': {'class': 'text-01'}},
#     {
#         'name': 'Titre 2 (SuisseU 44px)',
#         'element': 'h2',
#         'attributes': {'class': 'text-02'},
#     },
#     {
#         'name': 'Titre 3 (SuisseU 28px)',
#         'element': 'h3',
#         'attributes': {'class': 'text-05'},
#     },
#     {'name': 'Titre 4 (26px)', 'element': 'h4', 'attributes': {'class': 'text-07'}},
#     {
#         'name': 'Titre 6 / normal (16px)',
#         'element': 'p',
#         'attributes': {'class': 'text-08'},
#     },
#     {'name': 'Titre 6 (14px)', 'element': 'p', 'attributes': {'class': 'text-09'}},
#     {'name': 'Caché sur desktop', 'element': 'p',
#           'attributes': {'class': '@1-hidden'}},
# ]


# # for plugin
# CKEDITOR_SETTINGS = {
#     'language': '',
#     'toolbar': 'CMS',
#     'skin': 'moono-lisa',
#     'toolbarCanCollapse': False,
#     'format_tags': 'p;h1;h2;pre;address;div',
#     'stylesSet': CMS_EDITOR_STYLE_SET,
# }

# # for django-ckeditor
# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono',
#         # 'skin': 'office2013',
#         'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'styles', 'items': ['Format', 'Styles']},
#             {
#                 'name': 'document',
#                 'items': [
#                     'Source',
#                     '-',
#                     'Save',
#                     'NewPage',
#                     'Preview',
#                     'Print',
#                     '-',
#                     'Templates',
#                 ],
#             },
#             {
#                 'name': 'clipboard',
#                 'items': [
#                     'Cut',
#                     'Copy',
#                     'Paste',
#                     'PasteText',
#                     'PasteFromWord',
#                     '-',
#                     'Undo',
#                     'Redo',
#                 ],
#             },
#             {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
#             '/',
#             {
#                 'name': 'basicstyles',
#                 'items': [
#                     'Bold',
#                     'Italic',
#                     'Underline',
#                     'Strike',
#                     'Subscript',
#                     'Superscript',
#                     '-',
#                     'RemoveFormat',
#                 ],
#             },
#             {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList']},
#             {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#             {'name': 'insert', 'items': ['Image', 'HorizontalRule', 'SpecialChar']},
#             {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
#         ],
#         'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
#         'tabSpaces': 4,
#         'extraPlugins': ','.join(
#             [
#                 'uploadimage',  # the upload image feature
#                 # your extra plugins here
#                 'div',
#                 'autolink',
#                 'autoembed',
#                 'embedsemantic',
#                 'autogrow',
#                 # 'devtools',
#                 'widget',
#                 'lineutils',
#                 'clipboard',
#                 'dialog',
#                 'dialogui',
#                 'elementspath',
#             ]
#         ),
#         'stylesSet': CMS_EDITOR_STYLE_SET,
#     }
# }


# VALID_MARGINS = [
#     ('margin-top-01', 'Marge: 15px'),
#     ('margin-top-02', 'Marge: 30px'),
#     ('margin-top-03', 'Marge: 45px'),
#     ('margin-top-04', 'Marge: 60px'),
#     ('margin-top-05', 'Marge: 90px'),
#     ('margin-top-06', 'Marge: 120px'),
# ]
