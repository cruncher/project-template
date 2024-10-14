from django.db import models

from wagtail.models import Page
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    pass

# @register_setting
# class SiteSettings(BaseSiteSetting):
#     title_suffix = models.CharField(
#         verbose_name="Title suffix",
#         max_length=255,
#         help_text="The suffix for the title meta tag e.g. ' | Cruncher'",
#         default="Cruncher",
#     )

#     panels = [
#         FieldPanel("title_suffix"),
#     ]



# @register_setting
# class SiteSettings(BaseSiteSetting):
#     title_suffix = models.CharField(
#         verbose_name="Title suffix",
#         max_length=255,
#         help_text="The suffix for the title meta tag e.g. ' | Cruncher'",
#         default="Cruncher",
#     )

#     panels = [
#         FieldPanel("title_suffix"),
#     ]


# @register_setting
# class FooterSettings(BaseGenericSetting):
#     pass

# class FooterLink(models.Model):
#     setting = models.ForeignKey(FooterSettings, related_name="links", on_delete=models.CASCADE)
#     text = models.CharField(_("Texte"), max_length=50)
#     url = models.URLField(_("URL"), max_length=1024)