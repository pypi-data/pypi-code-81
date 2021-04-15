
from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from customers.forms import CustomerSelectForm

from basement.admin import admin_render_view, render
from basement.forms import get_clean_data
from basement.http import JsonResponse
from basement.views import FormActionView, ActionView, FilterView

from invoices import forms
from invoices.models import Sale, Arrival

from apps.products.models import Product


@staff_member_required
def create_invoice(request, invoice_type):

    invoices = request.env.invoices

    form = forms.InvoiceTypeSelectForm(
        invoices.get_model_types(invoice_type),
        request.POST)

    data = get_clean_data(form)

    invoice = invoices.create_invoice(invoice_type, data['type'])

    return redirect(invoice.manage_url)


@staff_member_required
def manage_invoice(request, invoice_type, invoice_id):

    invoice = request.env.invoices.get_invoice(invoice_type, invoice_id)

    expire_date = datetime.now().date() - timedelta(days=1)

    if not request.user.is_superuser and invoice.created.date() < expire_date:
        return HttpResponseForbidden(_('You can manage today`s invoices only'))

    customer_select_form = CustomerSelectForm(
        initial={'customer': invoice.customer})

    return render(request, 'invoices/manage/{}.html'.format(invoice_type), {
        'invoice': invoice,
        'invoice_type': invoice_type,
        'customer_select_form': customer_select_form
    })


set_customer = FormActionView(
    message=_('Customer saved'),
    form_class=CustomerSelectForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.invoices.set_customer(
            customer=cleaned_data['customer'],
            **url_kwargs)
)


set_discount = FormActionView(
    message=_('Discount saved'),
    form_class=forms.SetDiscountForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.invoices.set_discount(
            value=cleaned_data['value'],
            **url_kwargs)
)


add_item = FormActionView(
    message=_('Discount saved'),
    form_class=forms.ProductSelectForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.invoices.add_item(
            product=cleaned_data['product'],
            **url_kwargs)
)


set_item_qty = FormActionView(
    message=_('Quantity updated'),
    form_class=forms.SetQtyForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.invoices.set_item_qty(
            value=cleaned_data['value'],
            **url_kwargs)
)


set_item_price = FormActionView(
    message=_('Quantity updated'),
    form_class=forms.SetPriceForm,
    action=lambda request, url_kwargs, cleaned_data:
        request.env.invoices.set_item_price(
            value=cleaned_data['value'],
            **url_kwargs)
)


remove_item = ActionView(
    message=_('Item removed'),
    action=lambda request, url_kwargs, cleaned_data:
        request.env.invoices.remove_item(**url_kwargs)
)


get_products = FilterView(
    form_class=forms.SearchProductForm,
    search_iterator=lambda request, url_kwargs, cleaned_data:
        Product.objects.active().search(**cleaned_data),
    items_template='invoices/product-items.html',
    decorators=[staff_member_required]
)


@staff_member_required
def add_product(request):

    form = forms.AddProductForm(request.POST or None)

    status_code = 200

    if request.method == 'POST':

        if form.is_valid():

            product = form.save()

            return JsonResponse({
                'message': _('Product added'),
                'product_id': product.pk
            })
        else:
            status_code = 403

    return render(
        request,
        'invoices/add-product.html',
        {'form': form, 'status_code': status_code},
        status=status_code)


@staff_member_required
def add_customer(request):

    form = forms.AddCustomerForm(request.POST or None)

    status_code = 200

    if request.method == 'POST':

        if form.is_valid():

            customer = form.save()

            return JsonResponse({
                'message': _('Customer added'),
                'customer': {
                    'id': customer.pk,
                    'name': str(customer)
                }
            })
        else:
            status_code = 403

    return render(
        request,
        'invoices/add-customer.html',
        {'form': form, 'status_code': status_code},
        status=status_code)


@admin_render_view(template_name='invoices/print.html')
def print_invoice(request, invoice_type, invoice_id):
    return  {
        'invoice': request.env.invoices.get_invoice(invoice_type, invoice_id),
        'invoice_type': invoice_type
    }


def get_report(request, invoice_type):

    handlers = {
        'sale': get_sale_report,
        'arrival': get_arrival_report
    }

    try:
        handler = handlers[invoice_type]
    except KeyError:
        raise Exception('Unknown invoice type: {}'.format(invoice_type))

    return handler(request, invoice_type)


@admin_render_view(template_name='invoices/report/sale-report.html')
def get_sale_report(request, invoice_type):

    form = forms.ReportForm(request)

    data = get_clean_data(form)

    date_from = data['date_from']
    date_to = data['date_to']

    invoices = request.env.invoices

    items = invoices.get_invoice_items(
        'sale',
        date_from,
        date_to,
        exclude_categories=[
            Sale.TYPE_CUSTOM,
            Sale.TYPE_DEBT,
            Sale.TYPE_WRITE_OFF
        ])

    totals = invoices.get_invoice_totals(items)

    return_items = invoices.get_invoice_items(
        'arrival',
        date_from,
        date_to,
        category=Arrival.TYPE_RETURN)

    return_totals = invoices.get_invoice_totals(return_items)

    write_off_items = invoices.get_invoice_items(
        'sale',
        date_from,
        date_to,
        category=Sale.TYPE_WRITE_OFF)

    write_off_totals = invoices.get_invoice_totals(write_off_items)

    context = {
        'form': form,
        'items': items,
        'totals': totals,
        'return_items': return_items,
        'return_totals': return_totals,
        'write_off_items': write_off_items,
        'write_off_totals': write_off_totals,
        'grand_totals': {
            'qty': totals['qty'] - return_totals['qty'],
            'wholesale_total': (
                totals['wholesale_total'] -
                return_totals['wholesale_total']),
            'retail_total': (
                totals['retail_total'] - return_totals['retail_total']),
            'profit_total': (
                totals['profit_total'] - return_totals['profit_total'])
        }
    }

    context.update(data)

    return context


@admin_render_view(template_name='invoices/report/arrival-report.html')
def get_arrival_report(request, invoice_type):

    form = forms.ReportForm(request)

    data = get_clean_data(form)

    date_from = data['date_from']
    date_to = data['date_to']

    invoices = request.env.invoices

    items = invoices.get_invoice_items(
        'arrival',
        date_from,
        date_to,
        exclude_categories=[Arrival.TYPE_CUSTOM])

    totals = invoices.get_invoice_totals(items)

    context = {
        'form': form,
        'items': items,
        'totals': totals
    }

    context.update(data)

    return context
