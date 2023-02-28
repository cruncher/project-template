from apps.cruncher.admin import ParlerAllTranslationsMixin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Article, NewsCategory


@admin.register(Article)
class ArticleAdmin(
    TranslatableAdmin,
    ParlerAllTranslationsMixin,
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        "__str__",
        "category",
        "status",
        "publication_date",
        "all_translations",
    )
    list_filter = ("category", "status")


@admin.register(NewsCategory)
class NewsCategoryAdmin(
    TranslatableAdmin, ParlerAllTranslationsMixin, admin.ModelAdmin
):
    list_display = ("__str__", "order", "all_translations")
