from django.conf import settings
from django.utils.html import format_html_join


class ParlerAllTranslationsMixin(object):
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
                    "rgb(94, 136, 157)"
                    if lang in actual_codes
                    else "rgb(149, 186, 204)",
                    obj.pk,
                    lang,
                    lang.upper(),
                )
                for lang in _all_translations
            ],
        )

    all_translations.short_description = "Translations"
