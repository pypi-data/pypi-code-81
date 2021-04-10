#encoding:utf-8
from django import forms
from django.contrib.auth.models import Permission
from django.conf import settings


def getInstalledApps():
    apps_dict = {
        'djmicrosip_reorden': 'reorden',
        'django_microsip_diot': 'diot',
    }
    installed_apps = []
    for app_key in settings.EXTRA_MODULES:
        if app_key in apps_dict.keys():
            installed_apps.append(apps_dict[app_key])
    return installed_apps


class UsuarioForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), )

    def __init__(self, *args, **kwargs):
        permisos = []
        for permission in Permission.objects.filter(content_type__app_label__in=getInstalledApps()):
            permisos.append((permission.id, permission.name))
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['permisos'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=permisos, )
