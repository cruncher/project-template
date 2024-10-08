from django import forms


class SelectButton(forms.Select):
    template_name = "widgets/select-button.html"


class RadioSelect(forms.RadioSelect):
    template_name = "widgets/radio-select.html"

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs", {})
        attrs["class"] = "masked"
        attrs["label_class"] = attrs.get("label_class", "") or ""
        kwargs["attrs"] = attrs

        super().__init__(*args, **kwargs)


class Checkbox(forms.CheckboxInput):
    template_name = "widgets/checkbox.html"

    def __init__(self, *args, **kwargs):
        attrs = kwargs.get("attrs", {})
        attrs["class"] = "masked"
        attrs["label_class"] = attrs.get("label_class", "") or ""
        kwargs["attrs"] = attrs

        super().__init__(*args, **kwargs)


# WIP
class IncrementControlButton(forms.NumberInput):
    template_name = "widgets/increment-control.html"

    def __init__(self, *args, **kwargs):
        print(self, args, kwargs)
        super().__init__(*args, **kwargs)
