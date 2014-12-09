from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^$', '{{project_name}}.views.home', name='home'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^front-edit/', include('front.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(r'^404.html', TemplateView.as_view(template_name='404.html')),
        url(r'^style/', include('apps.styleguide.urls')),
        url(r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/img/', 'path': 'favicon.ico'}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
