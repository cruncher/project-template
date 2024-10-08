
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from django.contrib import admin
{%- if cookiecutter.use_parler %}
from apps.cruncher.admin import ParlerAllTranslationsMixin
from parler.admin import TranslatableAdmin
{%- endif %}
from .models import Article, NewsCategory


@admin.register(Article)
class ArticleAdmin(
    {%- if cookiecutter.use_parler %}
    TranslatableAdmin,
    ParlerAllTranslationsMixin,
    {%- endif %}
    PlaceholderAdminMixin,
    admin.ModelAdmin,
):
    list_display = (
        "__str__",
        "category",
        "status",
        "publication_date",
        {%- if cookiecutter.use_parler %}
        "all_translations",
        {%- endif %}
    )
    list_filter = ("category", "status")


@admin.register(NewsCategory)
class NewsCategoryAdmin(
    {%- if cookiecutter.use_parler %}TranslatableAdmin, ParlerAllTranslationsMixin,{%- endif %} admin.ModelAdmin
):
    list_display = ("__str__", "order", {%- if cookiecutter.use_parler %}"all_translations"{%- endif %} )
