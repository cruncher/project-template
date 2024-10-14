from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.timezone import now as utc_now

from .models import Article, ArticleStatuses
from .models import RecentNewsArticlesPlugin as RecentNewsArticlesPluginModel


@plugin_pool.register_plugin
class RecentNewsArticlesPlugin(CMSPluginBase):
    model = RecentNewsArticlesPluginModel
    name = "Recent News Articles"
    render_template = "news/recent-news-articles-plugin.html"
    filter_horizontal = ("categories",)

    def render(self, context, instance, placeholder):

        slides = Article.objects.filter(
            category__in=instance.categories.all(),
            status=ArticleStatuses.published,
            publication_date__lte=utc_now(),
        )

        context.update({"instance": instance, "slides": slides})
        return context
