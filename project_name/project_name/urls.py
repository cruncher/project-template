from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.static import serve as static_serve

from django_otp.admin import OTPAdminSite

from apps.users.views.auth import login_view, logout_view


# Enforce 2FA only in production.
if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite

admin.autodiscover()


urlpatterns = i18n_patterns(
    url(r"^admin/rosetta/", include("rosetta.urls")),
    url(r"^admin$", RedirectView.as_view(url="/admin/")),
    url(r"^admin/", admin.site.urls),
    url(r"^login/", login_view, name="auth.login"),
    url(r"^logout/", logout_view, name="auth.logout"),
    url(r"^password-reset/", include("apps.users.urls.password_reset")),
)

urlpatterns += [
    url(r"^i18n/", include("django.conf.urls.i18n")),
    url(r"^impersonate/", include("impersonate.urls")),
    url(r"^filer/", include("filer.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        url(r"^404.html", TemplateView.as_view(template_name="404.html")),
        url(
            r"^favicon.ico$",
            static_serve,
            {"document_root": settings.STATIC_ROOT + "/img/", "path": "favicon.ico"},
        ),
        url(
            r"^media/(?P<path>.*)$",
            static_serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
    ] + urlpatterns

    for prefix, root in settings.DEV_STATIC_URLS.items():
        urlpatterns.append(
            url(prefix, static_serve, {"document_root": root, "show_indexes": True})
        )
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [url(r"^rosetta/", include("rosetta.urls"))]

urlpatterns += i18n_patterns(url(r"^", include("cms.urls")))
