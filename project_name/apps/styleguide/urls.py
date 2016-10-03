from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^blocks/$', TemplateView.as_view(template_name='styleguide/style-blocks.html')),
    url(r'^forms/$', TemplateView.as_view(template_name='styleguide/style-forms.html')),
    url(r'^$', TemplateView.as_view(template_name='styleguide/style.html')),
]
