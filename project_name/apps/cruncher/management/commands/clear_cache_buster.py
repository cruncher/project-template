import string

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from apps.cruncher.templatetags.cache_buster_tags import CACHE_BUSTER_KEY


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--buster", action="store", help="use this buster")

    def handle(self, **options):
        cb = options.get("buster") or get_random_string(
            length=8, allowed_chars=string.ascii_lowercase
        )
        cache.set(CACHE_BUSTER_KEY, cb, 31536000)
