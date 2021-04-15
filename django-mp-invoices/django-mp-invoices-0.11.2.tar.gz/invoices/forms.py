
from django import forms
from django.utils.translation import ugettext_lazy as _

from categories.models import Category
from cap.fields import DatePickerField
from basement.utils import get_date_from_request
from customers.models import Customer

from apps.products.models import Product


class SearchProductForm(forms.Form):

    code = forms.CharField(required=False)

    bar_code = forms.CharField(required=False)

    query = forms.CharField(required=False)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.HiddenInput)

    def clean(self):

        cleaned_data = {}

        for k, v in self.cleaned_data.items():
            if v:
                cleaned_data[k] = v

        return cleaned_data


class ReportForm(forms.Form):

    date_from = DatePickerField(label=_('Date from'))

    date_to = DatePickerField(label=_('Date to'))

    is_profit_included = forms.BooleanField(
        label=_('Include profit'),
        initial=False,
        required=False)

    is_wholesale_price_included = forms.BooleanField(
        label=_('Include wholesale price'),
        initial=False,
        required=False)

    is_discount_included = forms.BooleanField(
        label=_('Include discount'),
        initial=False,
        required=False)

    def __init__(self, request):

        super().__init__(
            data={
                'date_from': get_date_from_request(request, 'date_from'),
                'date_to': get_date_from_request(request, 'date_to'),
                'is_profit_included': request.GET.get('is_profit_included'),
                'is_discount_included': request.GET.get('is_discount_included'),
                'is_wholesale_price_included': request.GET.get(
                    'is_wholesale_price_included')
            }
        )


class InvoiceTypeSelectForm(forms.Form):

    def __init__(self, types, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['type'] = forms.ChoiceField(choices=types)


class ProductSelectForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())


class SetDiscountForm(forms.Form):
    value = forms.IntegerField()


class SetQtyForm(forms.Form):
    value = forms.FloatField()


class SetPriceForm(forms.Form):
    value = forms.FloatField()


class AddProductForm(forms.ModelForm):

    stock = forms.FloatField(label=_('Stock'), min_value=1)

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'stock',
            'price_retail'
        ]


class AddCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'vin',
            'discount'
        ]
