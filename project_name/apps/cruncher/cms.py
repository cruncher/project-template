from cms.models import Page
from cms.plugin_rendering import ContentRenderer

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.template import RequestContext
from django.test import RequestFactory


def render_placeholder(ph, language=settings.LANGUAGE_CODE, extra_context=None):
    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    request.current_page = Page.objects.first()
    request.LANGUAGE_CODE = language

    renderer = ContentRenderer(request)
    context = RequestContext(request)
    context["request"] = request

    if extra_context:
        context.update(extra_context)
    return renderer.render_placeholder(ph, context=context, language=language)


def render_placeholder_text(
    placeholder, language=settings.LANGUAGE_CODE, extra_context=None
):
    text = ""
    for plugin in placeholder.cmsplugin_set.filter(language=language):
        instance, plugin_type = plugin.get_plugin_instance()
        if hasattr(instance, "search_fields"):
            try:
                text += " ".join(
                    getattr(instance, field, "") for field in instance.search_fields
                )
            except Exception:
                pass
    return text
