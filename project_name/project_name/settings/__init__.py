from .base import *  # NOQA
from .cms import *  # NOQA
from .meta import *  # NOQA
from .s3 import *  # NOQA


try:
    from .local import *  # NOQA
except ImportError:
    pass
