from cms.models import CMSPlugin
from cms.models.fields import PlaceholderRelationField
from cms.utils.placeholder import get_placeholder_from_slot
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from meta.models import ModelMeta
from parler.models import TranslatableModel, TranslatedFields


class ArticleStatuses(models.IntegerChoices):
    draft = 0, _("Brouillon")
    published = 10, _("Publié")
    removed = 20, _("Supprimé")


class NewsCategory(TranslatableModel):
    order = models.IntegerField(default=0)
    translations = TranslatedFields(name=models.CharField(_("Name"), max_length=127))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("order",)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Article(ModelMeta, TranslatableModel):
    status = models.IntegerField(
        choices=ArticleStatuses.choices, default=ArticleStatuses.draft
    )
    category = models.ForeignKey(
        NewsCategory, related_name="articles", on_delete=models.PROTECT
    )
    publication_date = models.DateTimeField(blank=True, null=True)

    image = FilerImageField(on_delete=models.PROTECT)
    placeholders = PlaceholderRelationField()
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=512),
        chapeau=models.TextField(blank=True, null=True),
    )

    _metadata = {
        "title": "title",
        "description": "get_meta_description",
        "image": "get_meta_image",
    }

    def get_template(self):
        return "news/includes/structure.html"

    @cached_property
    def content(self):
        return get_placeholder_from_slot(self.placeholders, "content")

    def get_meta_description(self):
        return (self.chapeau or "")[
            : settings.DJANGO_CHECK_SEO_SETTINGS.get("meta_description_length")[1]
        ]

    def get_meta_image(self):
        if self.image:
            return self.image.url

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-publication_date",)
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def get_absolute_url(self):
        return reverse("news.details", args=(self.pk, slugify(self.__str__())))

    @cached_property
    def related_news(self):
        return Article.objects.filter(
            status=ArticleStatuses.published, category=self.category
        ).exclude(pk=self.pk)[:4]


class RecentNewsArticlesPlugin(CMSPlugin):
    categories = models.ManyToManyField(NewsCategory)
    count = models.IntegerField(default=5)

    def copy_relations(self, old_instance):
        self.categories.clear()

        for cat in old_instance.categories.all():
            self.categories.add(cat)
