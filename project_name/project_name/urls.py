from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.static import serve as static_serve

from {{project_name}}.views import home

admin.autodiscover()


urlpatterns = i18n_patterns(
    url(r'^$', home, name='home'),
    url(r'^admin$', RedirectView.as_view(url='/admin/')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^front-edit/', include('front.urls')),
]

if settings.DEBUG:
    urlpatterns = [

        url(r'^404.html', TemplateView.as_view(template_name='404.html')),
        url(r'^style/', include('apps.styleguide.urls')),
        url(r'^favicon.ico$', static_serve, {'document_root': settings.STATIC_ROOT + '/img/', 'path': 'favicon.ico'}),
        url(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ] + urlpatterns

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls')), ]
