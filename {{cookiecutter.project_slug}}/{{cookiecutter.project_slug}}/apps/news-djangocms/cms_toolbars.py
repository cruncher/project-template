from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from django.urls import reverse

from .models import Article


@toolbar_pool.register
class NewsArticleToolbar(CMSToolbar):
    def populate(self):
        if self.is_current_app:
            menu = self.toolbar.get_or_create_menu("News", "News")
            url = reverse("admin:news_article_changelist")
            menu.add_sideframe_item("All news articles", url=url)
            if self.toolbar.obj and type(self.toolbar.obj) == Article:
                menu.add_sideframe_item(
                    "Edit %s" % self.toolbar.obj,
                    url=url + str(self.toolbar.obj.pk) + "/",
                )
