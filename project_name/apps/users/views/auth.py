from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import \
    PasswordResetView as DjangoPasswordResetView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from ..forms.auth import UserLoginForm


def login_view(request):
    next_ = request.GET.get('next', request.POST.get('next', '/'))
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.login_user(request)
            return HttpResponseRedirect(
                request.GET.get('next', form.cleaned_data.get('next', '/'))
            )
    else:
        form = UserLoginForm(initial={'next': next_})

    return render(
        request,
        'auth/login.html',
        {
            'form': form,
            'next': next_,
            'page_title_override': _('Connexion'),
            'current_page': 'auth.login',
        },
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class PasswordResetView(DjangoPasswordResetView):
    form_class = PasswordResetForm
