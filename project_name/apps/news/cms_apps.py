from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import re_path

from .views import details, home


@apphook_pool.register
class NewsApp(CMSApp):
    name = "News"

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            re_path(r"^$", home, name="news.home"),
            re_path(
                r"^cat/(?P<category_id>\d+)/(?P<slug>[\w-]+)/$",
                home,
                name="news.home.category",
            ),
            re_path(r"^(?P<id>\d+)/(?P<slug>[\w-]+)/$", details, name="news.details"),
        ]
