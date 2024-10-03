from django import forms
from django.forms.utils import ErrorList
from django.utils.html import conditional_escape, format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class ImageForm(forms.Form):
    file = forms.ImageField()


class PastedImageForm(forms.Form):
    data = forms.ImageField()


class FileForm(forms.Form):
    file = forms.FileField()


class CruncherErrorList(ErrorList):
    def __init__(self, initlist=None, error_class=None, renderer=None, html_id=None):
        self._html_id = html_id
        super().__init__(initlist=initlist, error_class=error_class, renderer=renderer)

    def as_flat(self):
        return self.as_ul()

    def as_ul(self):
        if not self.data:
            return ""

        return format_html_join(
            "{}",
            '<label {} class="error-label">{}</label>',
            (
                ("for={}".format(self._html_id) if self._html_id else "", e)
                for e in self
            ),
        )


class CruncherFormRenderer(forms.Form):
    def __init__(
        self,
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        field_order=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super().__init__(
            data=data,
            files=files,
            auto_id=auto_id,
            prefix=prefix,
            initial=initial,
            error_class=CruncherErrorList,
            label_suffix=label_suffix,
            empty_permitted=empty_permitted,
            field_order=field_order,
            use_required_attribute=use_required_attribute,
            renderer=renderer,
        )

    def _html_output(
        self,
        normal_row,
        error_row,
        row_ender,
        help_text_html,
        errors_on_separate_row=True,
    ):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = (
            self.non_field_errors()
        )  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ""
            bf = self[name]
            bf_errors = self.error_class(bf.errors, html_id=bf.id_for_label)
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [
                            _("(Hidden field %(name)s) %(error)s")
                            % {"name": name, "error": str(e)}
                            for e in bf_errors
                        ]
                    )
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if bf.label:
                    label = conditional_escape(bf.label)
                    label = bf.label_tag(label) or ""
                else:
                    label = ""

                if field.help_text:
                    help_text = mark_safe(
                        '<label for="%s" class="help-label">%s</label>'
                        % (bf.id_for_label, field.help_text)
                    )
                else:
                    help_text = ""

                output.append(
                    normal_row
                    % {
                        "errors": "",
                        "label": label,
                        "field": bf,
                        "help_text": help_text,
                        "html_class_attr": html_class_attr,
                        "css_classes": css_classes,
                        "field_name": bf.html_name,
                    }
                )

                if bf_errors:
                    output.append(error_row % str(bf_errors))

        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = "".join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = normal_row % {
                        "errors": "",
                        "label": "",
                        "field": "",
                        "help_text": "",
                        "html_class_attr": html_class_attr,
                        "css_classes": "",
                        "field_name": "",
                    }
                    output.append(last_row)
                output[-1] = last_row[: -len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe("\n".join(output))
