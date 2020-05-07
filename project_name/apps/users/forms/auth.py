import os
from email.mime.image import MIMEImage

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import \
    PasswordResetForm as DjangoPasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import gettext_lazy as _

from apps.cruncher.forms import CruncherFormRenderer


UserModel = get_user_model()


class UserLoginForm(CruncherFormRenderer):
    email = forms.EmailField(
        label=_('Votre adresse e-mail'),
        required=True,
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_('Mot de passe'),
        widget=forms.PasswordInput(),
        help_text='<a class="link-text" href="/password-reset/">{}</a>'.format(
            _('Perdu votre mot de passe?')
        ),
    )
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        email, password = (
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
        user = authenticate(request=None, email=email, password=password)
        if user is None:
            self.add_error('password', _('Adresse e-mail ou mot de passe invalides'))

    def login_user(self, request):
        assert self.is_bound
        email, password = (
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
        user = authenticate(request=request, email=email, password=password)
        if user.is_active:
            login(request, user)
            return user


class PasswordResetForm(CruncherFormRenderer, DjangoPasswordResetForm):
    email = forms.EmailField(label=_('Votre adresse e-mail'), required=True)

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        "Send a django.core.mail.EmailMultiAlternatives to `to_email`."

        context.update(BASE_URL=settings.BASE_URL)
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

            img = open(
                os.path.join(settings.BASE_DIR, 'static', 'images', 'email-logo.png'),
                'rb',
            ).read()
            logo_image = MIMEImage(img)
            logo_image.add_header('Content-ID', '<email-logo.png>')
            logo_image.add_header(
                'Content-Disposition', 'inline', filename='email-logo.png'
            )
            logo_image.add_header('Content-Type', 'image/png', name='email-logo.png')
            email_message.attach(logo_image)

        email_message.mixed_subtype = "related"
        email_message.send()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = UserModel.objects.filter(email=email)
        if users.exists():
            user = users.first()
            if user.is_active and not user.has_usable_password():
                raise forms.ValidationError(
                    _(
                        'Un utilisateur avec cette adresse e-mail existe, mais aucun mot de passe n\'y est associé. Vous êtes-vous inscrits en utilisant un compte Google ou Facebook? Si c\'est le cas, veuillez vous re-connecter en utilisant la même méthode!'
                    )
                )

        return email
