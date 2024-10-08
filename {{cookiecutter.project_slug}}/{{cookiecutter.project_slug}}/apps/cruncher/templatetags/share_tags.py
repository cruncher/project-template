from urllib.parse import quote as url_quote

from django import template
from django.conf import settings

register = template.Library()


def title_and_url(obj):
    try:
        url = (settings.BASE_URL or "") + obj.get_absolute_url()
    except Exception:
        url = None
    try:
        title = obj.__str__()
    except Exception:
        title = None

    return url, title


@register.filter
def share_on_twitter(obj):
    url, title = title_and_url(obj)
    return "https://twitter.com/intent/tweet?text=" + url_quote(
        ((title or "") + " " + (url or "")).strip()
    )


@register.filter
def share_on_linkedin(obj):
    url, __ = title_and_url(obj)
    return f"https://www.linkedin.com/sharing/share-offsite/?url={url_quote(url)}"


@register.filter
def share_on_facebook(obj):
    url, __ = title_and_url(obj)
    return f"https://www.facebook.com/sharer/sharer.php?u={url_quote(url)}"


@register.filter
def share_by_email(obj):
    url, title = title_and_url(obj)
    return f"mailto:?body={url_quote(url)}&subject={url_quote(title)}"
