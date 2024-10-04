from django.db import models
from wagtail.models import Page
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import  TagBase, ItemBase
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
{%- if cookiecutter.add_submodule_slideshow %}
from .blocks import  SlideShowBlock
{%- endif %}
from wagtail.search import index

# https://docs.wagtail.org/en/stable/reference/pages/model_recipes.html#custom-tag-models
# Basically we use custom tag so that autocomplete will not suggest all the tags but only
# article tags for articles. In case we use taggit in multiple models...
class ArticleTag(TagBase):
    class Meta:
        verbose_name = _("Etiquette d'article")
        verbose_name = _("Etiquettes d'article")

class TaggedArticle(ItemBase):
    tag = models.ForeignKey(
        ArticleTag, related_name="tagged_articles", on_delete=models.CASCADE
    )
    content_object = ParentalKey(to="news.ArticlePage", on_delete=models.CASCADE, related_name="tagged_articles")

class ArticlePage(Page):
    tags = ClusterTaggableManager(through=TaggedArticle, blank=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Landscape mode only; horizontal width between 1000px and 3000px."),
    )
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('publication_date'),
    ]
    body = StreamField([
        ("heading", blocks.CharBlock(form_classname="title")),
        ("paragraph", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
        {%- if cookiecutter.add_submodule_slideshow %}
        ("slideshow", SlideShowBlock())
        {%- endif %}
        ])
    promote_panels = Page.promote_panels + [
        FieldPanel("tags"),
        PageChooserPanel('related_page', 'news.ArticlePage'),
    ]

    related_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("image"),
        FieldPanel("body"),
    ]

