import re

from cms.models.pagemodel import Page
from easy_thumbnails.files import get_thumbnailer
from haystack import indexes

from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from django.utils.encoding import force_text
from django.utils.translation import activate


rf = RequestFactory()


class PageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=False)
    url = indexes.CharField(stored=True, indexed=False, model_attr="get_absolute_url")
    title = indexes.CharField(stored=True, indexed=True, model_attr="get_title")
    image = indexes.CharField(use_template=False, null=True)
    excerpt = indexes.CharField(use_template=False, null=True)
    type = indexes.CharField(use_template=False, null=True, faceted=True)
    date = indexes.DateField(null=True, use_template=False)

    def fancy_strip_tags(self, str_):
        return re.sub(r"<[^>]*?>", " ", force_text(str_))

    def prepare(self, obj, lang):
        request = rf.get("/")
        request.session = {}
        request.LANGUAGE_CODE = lang
        request.current_page = obj
        request.user = AnonymousUser()
        activate(lang)

        text = ""
        self.prepared_data = super(PageIndex, self).prepare(obj)

        self.prepared_data["type"] = "page"
        self.prepared_data["date"] = (
            obj.publication_date and obj.publication_date.date() or None
        )

        for placeholder in obj.placeholders.all():
            for plugin in placeholder.cmsplugin_set.filter(language=lang):
                instance, plugin_type = plugin.get_plugin_instance()

                if hasattr(instance, "search_fields"):
                    try:
                        text += " ".join(
                            getattr(instance, field) for field in instance.search_fields
                        )
                    except Exception:
                        pass

            for plugin in placeholder.cmsplugin_set.filter(
                language=lang, plugin_type="BannerPlugin"
            ):
                if self.prepared_data.get("image"):
                    continue

                instance, plugin_type = plugin.get_plugin_instance()
                if (
                    instance
                    and instance.image
                    and instance.style != "content-banner-block"
                ):
                    self.prepared_data["image"] = get_thumbnailer(instance.image)[
                        "feed-thumbs"
                    ].url

        excerpt = self.fancy_strip_tags(text.replace("\n", " ").replace("\t", " "))
        if len(excerpt) > 400:
            excerpt = excerpt[:400] + "…"
        self.prepared_data["excerpt"] = excerpt

        self.prepared_data["text"] = self.fancy_strip_tags(
            obj.get_title(language=lang) + " " + text
        )

        self.prepared_data["title"] = self.fancy_strip_tags(self.prepared_data["title"])

        # fixme: set the correct self.prepared_data['tab'] using this:
        # print  [p.get_slug() for p in obj.get_ancestors()] + [obj.get_slug()]
        if self.prepared_data["text"] and self.prepared_data["title"]:
            return self.prepared_data

    def index_queryset(self, lang, *args, **kwargs):
        page_ids = set()
        for p in Page.objects.published().filter(login_required=False).distinct():
            if p.get_public_object() and not p.get_redirect(lang):
                page_ids.add(p.get_public_object().pk)
        return Page.objects.filter(pk__in=list(page_ids))

    def get_model(self):
        return Page


class FrPageIndex(PageIndex, indexes.Indexable):
    def prepare(self, obj):
        return super().prepare(obj, "fr")

    def index_queryset(self, *args, **kwargs):
        return super().index_queryset("fr", *args, **kwargs)


class EnPageIndex(PageIndex, indexes.Indexable):
    def prepare(self, obj):
        return super().prepare(obj, "en")

    def index_queryset(self, *args, **kwargs):
        return super().index_queryset("en", *args, **kwargs)
