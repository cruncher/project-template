from django import template
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language
from ..timestamps import to_timestamp
from django.utils.safestring import mark_safe
from decimal import Decimal
import datetime


register = template.Library()


@register.filter
def dispaly_navigation(page):
    # page is level 1 and has children or we're on a leaf page
    return page and page.get_ancestors() and page.get_children_count() or page.get_ancestors().count() >= 2


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    url_parts = resolve(path)

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
    finally:
        activate(cur_language)

    ret = "%s" % url
    if context['request'] and context['request'].GET:
        ret += '?'
        get_items = []
        for k, v in context['request'].GET.iteritems():
            get_items.append('{}={}'.format(k, v))
        ret += '&'.join(get_items)
    return ret


# @register.filter
# def currency_conversion_rate(from_, to_):
#     return currency_convert(Decimal(1.0), to_, from_)


@register.filter(name='to_timestamp')
def to_timestamp_filter(dt):
    return to_timestamp(dt)


@register.filter(name='pk_list')
def pk_list(qs):
    return ','.join([str(v) for v in qs.values_list('id', flat=True).order_by('id')])


@register.filter(name='is_empty')
def is_empty(qs):
    return not qs.exists()


@register.filter(name='get_by_index')
def get_by_index(iterable, idx):
    return iterable[int(idx)]


@register.filter
def int_mult(a, b):
    return int(a or 0) * int(b or 0)


@register.filter
def fraction(dec, tag=None):
    d = Decimal(dec.replace(',', '.')).to_eng_string()
    if d[-2:] == '.5':
        if tag:
            return mark_safe('{}<{}>{}</{}>'.format(d[:-2], tag, '½', tag))
        return d[:-2] + '½'
    return dec


@register.filter
def int_div(a, b):
    return int(a) // int(b)


@register.filter
def add_hours(dt, hours):
    return dt + datetime.timedelta(hours=int(hours))
