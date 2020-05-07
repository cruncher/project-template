from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy

from ..forms.auth import PasswordResetForm


urlpatterns = [
    url(
        r'^$',
        auth_views.PasswordResetView.as_view(
            **{
                'template_name': 'password-reset/password-reset-form.html',
                'email_template_name': 'password-reset/password-reset-email.txt',
                'html_email_template_name': 'password-reset/password-reset-email.html',
                'form_class': PasswordResetForm,
                'success_url': reverse_lazy('users.password-reset-sent'),
            }
        ),
        name='users.password_reset',
    ),
    url(
        r'^new-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            **{
                'template_name': 'password-reset/password-reset-new-password.html',
                'form_class': SetPasswordForm,
                'success_url': reverse_lazy('users.password-reset-complete'),
            }
        ),
        name='users.password-reset-confirm',
    ),
    url(
        r'^sent/$',
        auth_views.PasswordResetDoneView.as_view(
            **{'template_name': 'password-reset/password-reset-done.html'}
        ),
        name='users.password-reset-sent',
    ),
    url(
        r'^complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            **{'template_name': 'password-reset/password-reset-complete.html'}
        ),
        name='users.password-reset-complete',
    ),
]
