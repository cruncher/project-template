from crispy_forms.utils import render_field, flatatt, TEMPLATE_PACK
from crispy_forms.layout import LayoutObject
from django.template.loader import render_to_string


class FormActions(LayoutObject):
    """
    Bootstrap layout object. It wraps fields in a <div class="form-actions">

    Example::

        FormActions(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save', css_class='btn-primary')
        )
    """
    template = "%s/layout/formactions.html" % TEMPLATE_PACK

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.template = kwargs.pop('template', self.template)
        self.attrs = kwargs
        if 'css_class' in self.attrs:
            self.attrs['class'] = self.attrs.pop('css_class')

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        html = u''
        for field in self.fields:
            html += '<li>' + render_field(field, form, form_style, context, template_pack=template_pack) + '</li>'

        return render_to_string(self.template, {'formactions': self, 'fields_output': html})

    def flat_attrs(self):
        return flatatt(self.attrs)
