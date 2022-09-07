from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.static import serve as static_serve

from django_otp.admin import OTPAdminSite

from apps.cruncher.views import template_folder
from apps.users.views.auth import login_view, logout_view


# Enforce 2FA only in production.
if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite

admin.autodiscover()


urlpatterns = i18n_patterns(
    re_path(r"^admin/rosetta/", include("rosetta.urls")),
    re_path(r"^admin$", RedirectView.as_view(url="/admin/")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^login/", login_view, name="auth.login"),
    re_path(r"^logout/", logout_view, name="auth.logout"),
    re_path(r"^password-reset/", include("apps.users.urls.password_reset")),
    re_path(r"^test/(?P<path>.*)$", template_folder, {"document_root": "test"}),
)

urlpatterns += [
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
    re_path(r"^impersonate/", include("impersonate.urls")),
    re_path(r"^filer/", include("filer.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        re_path(r"^404.html", TemplateView.as_view(template_name="404.html")),
        re_path(
            r"^favicon.ico$",
            static_serve,
            {"document_root": settings.STATIC_ROOT + "/img/", "path": "favicon.ico"},
        ),
        re_path(
            r"^media/(?P<path>.*)$",
            static_serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
    ] + urlpatterns

    for prefix, root in settings.DEV_STATIC_URLS.items():
        urlpatterns.append(
            re_path(prefix, static_serve, {"document_root": root, "show_indexes": True})
        )
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

urlpatterns += i18n_patterns(re_path(r"^", include("cms.urls")))
