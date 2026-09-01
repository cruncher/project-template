from .base import *  # NOQA
# from .cms import *  # NOQA
{%- if cookiecutter.use_s3_storage %}
from .s3 import *  # NOQA
{%- endif %}
try:
    from .local import *  # noqa: F403
except ImportError:
    pass
