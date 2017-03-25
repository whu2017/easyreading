# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User

logger = logging.getLogger(__name__)


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='密码', strip=False, widget=forms.PasswordInput(attrs={'class': 'vTextField'}))

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        if not email and not phone:
            raise forms.ValidationError('Email 和手机号必须填写至少一个')

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and self._meta.model.objects.get_queryset().filter(email=email).exists():
            raise forms.ValidationError('Email 已存在，请更换一个新的 Email')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and self._meta.model.objects.get_queryset().filter(phone=phone).exists():
            raise forms.ValidationError('手机号已存在，请更换一个新的手机号')
        return phone

    def save(self, commit=True):
        return self._meta.model.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['phone'],
            self.cleaned_data['password'],
        )

    def save_m2m(self):
        pass


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='密码', help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        if not email and not phone:
            raise forms.ValidationError('Email 和手机号必须填写至少一个')

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == self.instance.email:
            return email
        if email and self._meta.model.objects.get_queryset().filter(email=email).exists():
            raise forms.ValidationError('Email 已存在，请更换一个新的 Email')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone == self.instance.phone:
            return phone
        if phone and self._meta.model.objects.get_queryset().filter(phone=phone).exists():
            raise forms.ValidationError('手机号已存在，请更换一个新的手机号')
        return phone

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = (
        'id', 'email', 'phone', 'nickname', 'is_superuser', 'option_sync_progress', 'option_clean_cache',
        'option_display_progress', 'option_wifi_download_only', 'option_accept_push', 'option_auto_buy_chapter',
    )
    list_filter = ()
    fieldsets = (
        ('基本信息', {
            'fields': ('email', 'phone', 'password'),
        }),
        ('个性设置', {
            'fields': ('nickname', 'signature'),
        }),
        ('个人选项', {
            'fields': (
                'option_sync_progress', 'option_clean_cache', 'option_display_progress',
                'option_wifi_download_only', 'option_accept_push', 'option_auto_buy_chapter',
            ),
        }),
    )
    add_fieldsets = (
        ('基本信息', {
            'fields': ('email', 'phone', 'password',),
        }),
        ('个性设置', {
            'fields': ('nickname', 'signature'),
        }),
        ('个人选项', {
            'classes': ('wide',),
            'fields': (
                'option_sync_progress', 'option_clean_cache', 'option_display_progress',
                'option_wifi_download_only', 'option_accept_push', 'option_auto_buy_chapter',
            ),
        }),
    )
    search_fields = ('email', 'phone', 'nickname')
    ordering = ('-id', )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
