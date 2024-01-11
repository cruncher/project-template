from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html_join


class ParlerAllTranslationsMixin(object):
    @admin.display(description="Translations")
    def all_translations(self, obj):
        _all_translations = [
            c.get("code") for c in settings.PARLER_LANGUAGES.get(settings.SITE_ID)
        ]

        actual_codes = list(obj.translations.values_list("language_code", flat=True))

        return format_html_join(
            " ",
            '<a style="border-radius: 3px; background-color: {}; '
            'color: #fff; padding: 2px 3px; font-size: smaller; " '
            'href="{}/change/?language={}">{}</a>',
            [
                (
                    "rgb(94, 136, 157)" if lang in actual_codes else "rgb(149, 186, 204)",
                    obj.pk,
                    lang,
                    lang.upper(),
                )
                for lang in _all_translations
            ],
        )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if hasattr(self, "copy_translations_on_save") and self.copy_translations_on_save:
            inst = form.instance
            current_lang = request.GET.get("language")

            translations = inst.translations.all()
            current_translation = translations.filter(language_code=current_lang).first()

            if inst and current_lang and current_translation:
                for lc, _ in settings.LANGUAGES:
                    if not translations.filter(language_code=lc).exists():
                        current_translation.pk = None
                        current_translation.language_code = lc
                        current_translation.save()
