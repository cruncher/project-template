from .base import *  # noqa
from .cms import *  # noqa
from .s3 import *  # noqa

try:
    from .local import *  # noqa
except ImportError:
    print("settings.local not found")

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "test_create_from_project_template",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
