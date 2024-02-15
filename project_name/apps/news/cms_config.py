from cms.app_base import CMSAppConfig
from . import models, views


class NewsAppConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_enabled_models = [(models.Article, views.render_details)]
