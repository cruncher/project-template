# encoding: utf-8
import datetime
from decimal import Decimal, ROUND_UP
import re

from django import template
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.template.defaultfilters import date
from django.utils.formats import number_format

register = template.Library()


@register.filter
def intapos(value):
    """
    Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    orig = smart_text(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>\'\g<2>', orig)
    if orig == new:
        return mark_safe(new)
    else:
        return intapos(new)
intapos.is_safe = True


@register.filter
def starts_with(a, b):
    try:
        return smart_text(a).startswith(smart_text(b))
    except:
        return False


@register.filter
def gt(a, b):
    try:
        return int(a) > int(b)
    except:
        return False


@register.filter
def lt(a, b):
    try:
        return int(a) < int(b)
    except:
        return False


@register.filter
def fancy_strip_tags(str_):
    return re.sub(r'<[^>]*?>', ' ', smart_text(str_))


@register.filter
def enumerate(list):
    return enumerate(list)


@register.filter
def line_break_after(words, word):
    split_words = words.split(' ')
    return mark_safe(' '.join(split_words[:int(word)]) + '<br />' + ' '.join(split_words[int(word):]))


@register.filter
def mult(a, b):
    return int(a) * int(b)


@register.filter
def fmult(a, b):
    return float(a) * float(b)


@register.filter
def fmulti(a, b):
    return int(float(a or 1.0) * float(b or 1.0))


@register.filter
def invert(a):
    return float(1) / float(a or '1.0')


@register.filter
def sub(a, b):
    return int(a) - int(b)


@register.filter
def asterisks(how_many):
    return int(how_many) * "*"


@register.filter
def round_up(val, to_):
    return (Decimal(val) / Decimal(to_)).quantize(Decimal('1'), rounding=ROUND_UP) * Decimal(to_)


@register.filter(name='str')
def to_str(v):
    return str(v)


@register.simple_tag
def days_in_future(days=0, format=''):
    return date(datetime.date.today() + datetime.timedelta(days=days), format)


@register.filter
def dict_key(dct, key):
    return dct.get(key)


@register.filter
def sub_days(date_, days):
    try:
        days = int(days)
        return date_ - datetime.timedelta(days=days)
    except:
        return date_


@register.filter
def json_floatformat(value, decimal_pos=4):
    return mark_safe(number_format(value, decimal_pos=decimal_pos, use_l10n=False))
