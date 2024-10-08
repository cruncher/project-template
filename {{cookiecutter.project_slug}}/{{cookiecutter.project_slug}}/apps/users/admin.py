from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import User


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'mobile_phone',
            'is_active',
            'is_staff',
            'is_superuser',
        )


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    ('mobile_phone', 'mobile_phone_validated'),
                )
            },
        ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': (('last_login', 'date_joined'),)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'impersonate')

    def impersonate(self, o):
        if o.is_superuser:
            return ''
        return format_html('<a href="/impersonate/{}/">GO</a>', o.pk)


admin.site.register(User, UserAdmin)
