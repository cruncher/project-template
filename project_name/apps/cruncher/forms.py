from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from apps.cruncher.layout import FormActions
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput
from django.utils.html import conditional_escape, html_safe
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.urls import reverse
import six


class ImageForm(forms.Form):
    file = forms.ImageField()


class PastedImageForm(forms.Form):
    data = forms.ImageField()


class FileForm(forms.Form):
    file = forms.FileField()


class CruncherFormRenderer(forms.Form):
    def layout(self, fieldname, col=1, row=1, span=4):
        self[fieldname].label_layout = (col, 2 * row, span)
        self[fieldname].layout = (col, 2 * row + 1, span)

        if hasattr(self, '_max_row'):
            self._max_row = max(self._max_row, 2 * row)
        else:
            self._max_row = 2 * row + 1

    def submit_button(self, value, classes='action-button button'):
        self._button = value
        self._button_classes = classes

    def render(self):
        return self._html_output(
            normal_row='%(label)s %(field)s%(help_text)s',
            error_row='%s',
            row_ender=' ',
            help_text_html=' <label class="help-label" for="%s">%s</label>',
            errors_on_separate_row=True)

    def _layout_classes(self, col, row, span):
        return ['col-{}'.format(col), 'row-{}'.format(row), 'span-{}'.format(span)]

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': force_text(e)}
                         for e in bf_errors])
                hidden_fields.append(six.text_type(bf))
            else:

                if bf.label:
                    label = conditional_escape(force_text(bf.label))
                    label_classes = []
                    if hasattr(bf, 'label_layout'):
                        col, row, span = bf.label_layout
                        label_classes = self._layout_classes(*bf.label_layout)

                    if field.required:
                        label_classes.append('required')

                    if label_classes:
                        label_attrs = {'class': ' '.join(label_classes)}
                    else:
                        label_attrs = None

                    label = bf.label_tag(label, attrs=label_attrs) or ''
                else:
                    label = ''

                field_classes = []
                if hasattr(bf, 'layout'):
                    field_classes = self._layout_classes(*bf.layout)

                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    field_classes.append(css_classes)

                if field_classes:
                    rendered_field_classes = ' '.join(field_classes)
                    html_class_attr = ' class="{}"'.format(rendered_field_classes)

                    if 'class' in field.widget.attrs:
                        field.widget.attrs['class'] = '{} {}'.format(field.widget.attrs['class'], rendered_field_classes)
                    else:
                        field.widget.attrs['class'] = rendered_field_classes


                # Replace the help text with the error, if any
                if field.help_text and not bf_errors:

                    help_text = help_text_html % (force_text(bf.id_for_label), force_text(field.help_text))
                else:
                    help_text = ''

                # We wrap selects, give them the field's classes
                if isinstance(field.widget, forms.Select):
                    field_class_ = field.widget.attrs.get('class', '')
                    field_html = '<label class="{} select-button button">{}</label>'.format(
                        field_class_,
                        six.text_type(bf)
                    )
                    field.widget.attrs['class'] = ''

                # Normal field
                else:
                    field_html = six.text_type(bf)

                output.append(normal_row % {
                    'errors': force_text(bf_errors),
                    'label': force_text(label),
                    'field': field_html,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })

                # Append under the field
                if bf_errors:
                    html_error = '<label class="error-label">{}</label>'.format(' '.join(bf_errors))
                    output.append(html_error)


        if top_errors:
            # import pudb
            # pudb.set_trace()
            output.insert(0, '<label class="error-label row-1 span-7 col-1">{}</label>'.format(
                '<br>'.join(top_errors)
            ))
            # output.insert(0, error_row % force_text(top_errors))

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors': '',
                        'label': '',
                        'field': '',
                        'help_text': '',
                        'html_class_attr': html_class_attr,
                        'css_classes': '',
                        'field_name': '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)

        if hasattr(self, '_button') and hasattr(self, '_button_classes'):
            cls_ = [self._button_classes] + self._layout_classes(0, self._max_row + 1, 2)
            output.append('<input type="submit" value="{}" class="{}" />'.format(self._button, ' '.join(cls_)))

        return mark_safe('\n'.join(output))
