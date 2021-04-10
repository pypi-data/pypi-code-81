#encoding:utf-8
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from .models import *
from dal import autocomplete

class LineaArticulosManageForm(forms.ModelForm):
    class Meta:
        model = LineaArticulos
        exclude= {
            'cuenta_ventas',
        }