from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.urls import re_path, reverse_lazy

from ..forms.auth import PasswordResetForm


urlpatterns = [
    re_path(
        r"^$",
        auth_views.PasswordResetView.as_view(
            **{
                "template_name": "password-reset/password-reset-form.html",
                "email_template_name": "password-reset/password-reset-email.txt",
                "html_email_template_name": "password-reset/password-reset-email.html",
                "form_class": PasswordResetForm,
                "success_url": reverse_lazy("users.password-reset-sent"),
            }
        ),
        name="users.password_reset",
    ),
    re_path(
        r"^new-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$",
        auth_views.PasswordResetConfirmView.as_view(
            **{
                "template_name": "password-reset/password-reset-new-password.html",
                "form_class": SetPasswordForm,
                "success_url": reverse_lazy("users.password-reset-complete"),
            }
        ),
        name="users.password-reset-confirm",
    ),
    re_path(
        r"^sent/$",
        auth_views.PasswordResetDoneView.as_view(
            **{"template_name": "password-reset/password-reset-done.html"}
        ),
        name="users.password-reset-sent",
    ),
    re_path(
        r"^complete/$",
        auth_views.PasswordResetCompleteView.as_view(
            **{"template_name": "password-reset/password-reset-complete.html"}
        ),
        name="users.password-reset-complete",
    ),
]
