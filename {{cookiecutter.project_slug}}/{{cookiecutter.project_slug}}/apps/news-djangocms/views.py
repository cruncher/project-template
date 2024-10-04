from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Article, ArticleStatuses, NewsCategory


def home(request, category_id=None, slug=None):
    category = None
    if category_id:
        category = get_object_or_404(NewsCategory, id=category_id)

    if request.user.is_staff:
        if category:
            articles = Article.objects.filter(
                status__in=(ArticleStatuses.published, ArticleStatuses.draft),
                category=category,
            ).translated()
        else:
            articles = Article.objects.filter(
                status__in=(ArticleStatuses.published, ArticleStatuses.draft)
            ).translated()

    else:
        if category:
            articles = Article.objects.filter(
                status=ArticleStatuses.published,
                category=category,
            ).translated()
        else:
            articles = Article.objects.filter(
                status=ArticleStatuses.published
            ).translated()

    template = "news/home.html"

    if request.headers.get("X-Is-Ajax"):
        template = "news/includes/articles.html"

    return render(
        request,
        template,
        {
            "articles": articles,
            "current_category": category,
            "categories": NewsCategory.objects.annotate(
                article_count=Count("articles")
            ).filter(article_count__gt=0),
        },
    )


def render_details(request, obj):  # Used by django cms
    return render(request, "news/details.html", {"article": obj, "meta": obj.as_meta()})


def details(request, id, slug):
    if request.user.is_staff:
        article = get_object_or_404(
            Article,
            id=id,
            status__in=(ArticleStatuses.published, ArticleStatuses.draft),
        )

    else:
        article = get_object_or_404(Article, id=id, status=ArticleStatuses.published)

    if hasattr(request, "toolbar"):
        request.toolbar.set_object(article)

    return render_details(request, article)
