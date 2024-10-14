from django import template, forms

register = template.Library()


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)
