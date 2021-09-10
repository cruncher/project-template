import string

from django import template
from django.core.cache import cache
from django.utils.crypto import get_random_string


register = template.Library()


CACHE_BUSTER_KEY = "cache-buster-{{project_name}}"


@register.simple_tag
def cache_buster():
    cb = cache.get(CACHE_BUSTER_KEY)
    if cb is None:
        cb = get_random_string(length=8, allowed_chars=string.ascii_lowercase)
        cache.set(CACHE_BUSTER_KEY, cb, 31536000)

    return str(cb)
