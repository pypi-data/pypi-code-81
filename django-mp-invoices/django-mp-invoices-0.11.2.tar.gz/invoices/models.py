
from datetime import datetime, time

from django.apps import apps
from django.utils.functional import cached_property
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from customers.models import CustomerField

from basement.services import register_service

from exchange.utils import get_price_factory
from exchange.constants import CURRENCY_UAH
from exchange.models import MultiCurrencyPrice, ExchangeRates


app_config = apps.get_app_config('invoices')


class InvoiceField(models.ForeignKey):

    def __init__(
            self,
            to,
            verbose_name=_('Invoice'),
            on_delete=models.CASCADE,
            related_name='items',
            *args, **kwargs):

        super().__init__(
            to=to,
            verbose_name=verbose_name,
            on_delete=on_delete,
            related_name=related_name,
            *args, **kwargs)


class InvoiceTypeField(models.PositiveIntegerField):

    def __init__(
            self,
            choices,
            verbose_name=_('Type'),
            *args, **kwargs):

        super().__init__(
            choices=choices,
            verbose_name=verbose_name,
            *args, **kwargs
        )


class Invoice(models.Model):

    type = NotImplemented
    customer = NotImplemented

    creator = models.ForeignKey(
        get_user_model(),
        verbose_name=_('Creator'),
        on_delete=models.PROTECT)

    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    discount = models.PositiveIntegerField(
        verbose_name=_('Discount, %'),
        default=0)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._old_type = self.type

    def save(self, **kwargs):
        if self.type != self._old_type:
            self.created = timezone.now()
        super().save(**kwargs)

    def __str__(self):
        return str(self.created)

    @classmethod
    def create(cls, type):
        return cls.objects.create(type=type)

    @property
    def customer_name(self):
        if self.customer:
            return self.customer.name
        return ''

    @property
    def invoice_type(self):
        return self.__class__.__name__.lower()

    @property
    def manage_url(self):
        return self._get_url('manage')

    @property
    def print_url(self):
        return self._get_url('print')

    @property
    def set_customer_url(self):
        return self._get_url('set-customer')

    @property
    def add_item_url(self):
        return self._get_url('add-item')

    @property
    def set_discount_url(self):
        return self._get_url('set-discount')

    def _get_url(self, name):
        return reverse_lazy('invoices:' + name, args=[
            self.invoice_type,
            self.pk
        ])

    @property
    def model_name(self):
        return self._meta.verbose_name

    @transaction.atomic
    def add_item(self, product, qty=1, update_product=True):
        try:
            item = self.items.get(product=product)
            item.qty += qty
            item.save()

        except ObjectDoesNotExist:
            item = self.items.create(
                product=product,
                qty=qty,
                **product.price_values
            )

        self._handle_add_item(product, qty, update_product=update_product)

        return item

    def _handle_add_item(self, product, qty, update_product):
        pass

    @transaction.atomic
    def set_item_qty(self, item_id, value):

        item = self.items.select_related('product').get(pk=item_id)

        if item.qty != value:
            self._handle_set_item_qty(item, value)

            item.qty = value
            item.save(update_fields=['qty'])

        return item

    @transaction.atomic
    def set_item_price(self, item_id, value):

        item = self.items.select_related('product').get(pk=item_id)

        if item.price_uah != value:
            self._handle_set_item_price(item, value)

            item.initial_currency = CURRENCY_UAH
            item.price_retail = value
            item.save()

        return item

    def _handle_set_item_qty(self, item, value):
        pass

    def _handle_set_item_price(self, item, value):
        pass

    @transaction.atomic
    def remove_item(self, item_id):

        item = self.items.select_related('product').get(pk=item_id)

        self._handle_remove_item(item)

        product = item.product

        item.delete()

        return product

    def _handle_remove_item(self, item):
        pass

    def set_customer(self, customer):

        self.customer = customer
        self.discount = self.customer_discount
        self.save(update_fields=['customer', 'discount'])

    @property
    def total(self):
        return sum([i.subtotal for i in self.items.all()])

    @property
    def discounted_total(self):
        return self.calculate_discount(self.total)

    @property
    def total_with_discount(self):
        return self.total - self.discounted_total

    @property
    def total_qty(self):
        return sum([i.qty for i in self.items.all()])

    @property
    def customer_discount(self):

        if self.customer:
            return self.customer.discount

        return 0

    def calculate_discount(self, number):

        if not self.discount:
            return 0

        return (self.discount * number) / 100.0

    def set_discount(self, value):
        self.discount = value
        self.save(update_fields=['discount'])

    def serialize_totals(self):
        return {
            'grand_total': self.total,
            'discount_percentage': self.discount,
            'discounted_total': self.discounted_total,
            'total_with_discount': self.total_with_discount
        }

    def get_items(self):
        return self.items.all().order_by('-id')

    class Meta:
        abstract = True


class InvoiceItem(MultiCurrencyPrice):

    invoice = NotImplemented

    product = models.ForeignKey(
        'products.Product',
        verbose_name=_('Product'),
        on_delete=models.CASCADE)

    qty = models.FloatField(_('Quantity'))

    def get_qty_input_value(self):
        return str(self.qty).replace(',', '')

    def set_rates(self, rates):
        self.rates = rates

    @cached_property
    def customer_name(self):
        return self.invoice.customer_name

    @cached_property
    def product_name(self):
        return self.product.name

    @property
    def bar_code(self):
        return self.product.bar_code

    @property
    def set_qty_url(self):
        return reverse_lazy('invoices:set-item-qty', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    @property
    def set_price_url(self):
        return reverse_lazy('invoices:set-item-price', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    @property
    def remove_url(self):
        return reverse_lazy('invoices:remove-item', args=[
            self.invoice.invoice_type,
            self.invoice.pk,
            self.pk
        ])

    def calculate_discount(self, number):
        return self.invoice.calculate_discount(number)

    @property
    def price(self):
        price = super().price

        if self.currency == CURRENCY_UAH:
            return round(price)

        return price

    @property
    def price_with_discount(self):
        return self.price - self.calculate_discount(self.price)

    @property
    def subtotal(self):
        return self.price * self.qty

    @property
    def discounted_subtotal(self):
        return self.calculate_discount(self.subtotal)

    @property
    def subtotal_with_discount(self):
        return self.price_with_discount * self.qty

    @property
    def price_wholesale_uah(self):
        return get_price_factory(
            self.rates,
            self.initial_currency,
            CURRENCY_UAH
        )(self.price_wholesale)

    @property
    def wholesale_subtotal_uah(self):
         return self.price_wholesale_uah * self.qty

    @property
    def profit_uah(self):
        return self.price_with_discount - self.price_wholesale_uah

    @property
    def profit_subtotal_uah(self):
        return self.subtotal_with_discount - self.wholesale_subtotal_uah

    @property
    def printable_qty(self):
        if hasattr(self.product, 'format_qty'):
            return self.product.format_qty(self.qty)

        return self.qty

    def render(self):
        return render_to_string('invoices/item.html', {'object': self})

    def serialize_product(self):
        return self.product.serialize()

    class Meta:
        abstract = True


class Arrival(Invoice):

    TYPE_INCOME = 1
    TYPE_RETURN = 2
    TYPE_CUSTOM = 3

    TYPES = (
        (TYPE_INCOME, _('Income')),
        (TYPE_RETURN, _('Return')),
        (TYPE_CUSTOM, _('Custom')),
    )

    type = InvoiceTypeField(TYPES)

    customer = CustomerField(related_name='arrivals')

    def _handle_add_item(self, product, qty, update_product):

        if update_product:
            product.add_stock(value=qty)

    def _handle_set_item_qty(self, item, value):

        if item.qty > value:
            item.product.subtract_stock(item.qty - value)
        else:
            item.product.add_stock(value - item.qty)

    def _handle_remove_item(self, item):

        if item.qty > 0:
            item.product.subtract_stock(item.qty)

    class Meta:
        verbose_name = _('Arrival invoice')
        verbose_name_plural = _('Arrival invoices')


class ArrivalItem(InvoiceItem):

    invoice = InvoiceField(Arrival)


class Sale(Invoice):

    TYPE_CASH_REGISTER = 1
    TYPE_WRITE_OFF = 2
    TYPE_ONLINE = 3
    TYPE_CUSTOM = 4
    TYPE_DEBT = 5

    TYPES = (
        (TYPE_CASH_REGISTER, _('Cash register')),
        (TYPE_WRITE_OFF, _('Write off')),
        (TYPE_DEBT, _('Debt')),
        (TYPE_CUSTOM, _('Custom')),
    )

    if app_config.is_online_sale_enabled:
        TYPES += ((TYPE_ONLINE, _('Online')), )

    type = InvoiceTypeField(TYPES)

    customer = CustomerField(related_name='sales')

    def _handle_add_item(self, product, qty, update_product):

        if update_product:
            product.subtract_stock(value=qty)

    def _handle_set_item_qty(self, item, value):

        if value > item.qty:
            item.product.subtract_stock(value - item.qty)
        else:
            item.product.add_stock(item.qty - value)

    def _handle_remove_item(self, item):

        if item.qty > 0:
            item.product.add_stock(item.qty)

    @property
    def service_total(self):
        return sum([s.subtotal for s in self.services.all()])

    def set_customer(self, customer):
        super().set_customer(customer)
        self.services.all().update(customer=customer)

    def serialize_totals(self):
        totals = super().serialize_totals()
        totals['service_total'] = self.service_total
        return totals

    class Meta:
        verbose_name = _('Sales invoice')
        verbose_name_plural = _('Sales invoices')


class SaleItem(InvoiceItem):

    invoice = InvoiceField(Sale)


class InvoicesService(object):

    def __init__(self, user):
        self._user = user
        self._check_access()

    def create_invoice(self, invoice_type, inner_type):
        model = self._get_invoice_model(invoice_type)
        return model.objects.create(type=inner_type, creator=self._user)

    def set_customer(self, invoice_type, invoice_id, customer):

        invoice = self.get_invoice(invoice_type, invoice_id)
        invoice.set_customer(customer)

        return {
            'total': invoice.serialize_totals()
        }

    def set_discount(self, invoice_type, invoice_id, value):

        invoice = self.get_invoice(invoice_type, invoice_id)
        invoice.set_discount(value)

        return {
            'total': invoice.serialize_totals()
        }

    def add_item(self, invoice_type, invoice_id, product):

        invoice = self.get_invoice(invoice_type, invoice_id)
        item = invoice.add_item(product)

        return {
            'status': 'OK',
            'html': item.render(),
            'item_id': item.id,
            'product': item.serialize_product(),
            'total': invoice.serialize_totals()
        }

    def set_item_qty(self, invoice_type, invoice_id, item_id, value):

        invoice = self.get_invoice(invoice_type, invoice_id)

        item = invoice.set_item_qty(item_id, value)

        return {
            'product': item.serialize_product(),
            'total': invoice.serialize_totals()
        }

    def set_item_price(self, invoice_type, invoice_id, item_id, value):

        invoice = self.get_invoice(invoice_type, invoice_id)

        item = invoice.set_item_price(item_id, value)

        return {
            'product': item.serialize_product(),
            'total': invoice.serialize_totals()
        }

    def remove_item(self, invoice_type, invoice_id, item_id):

        invoice = self.get_invoice(invoice_type, invoice_id)

        product = invoice.remove_item(item_id)

        return {
            'product': product.serialize(),
            'total': invoice.serialize_totals()
        }

    def get_invoice(self, invoice_type, invoice_id):

        model = self._get_invoice_model(invoice_type)

        try:
            return model.objects.get(pk=invoice_id)
        except ObjectDoesNotExist:
            raise Exception(_('Invoice not found'))

    def get_sale(self, sale_id):
        return self.get_invoice('sale', sale_id)

    def get_model_types(self, invoice_type):
        model = self._get_invoice_model(invoice_type)
        return model.TYPES

    def get_invoice_items(
            self,
            invoice_type,
            date_from,
            date_to,
            category=None,
            exclude_categories=None):

        model = self._get_invoice_model(invoice_type)

        invoices = model.objects.filter(
            created__date__range=[date_from, date_to]
        ).prefetch_related(
            'items',
            'items__product'
        )

        if category is not None:
            invoices = invoices.filter(type=category)

        if exclude_categories is not None:
            invoices = invoices.exclude(type__in=exclude_categories)

        invoices = invoices.order_by('created')

        result = []
        rates = ExchangeRates.objects.get()

        for invoice in invoices:
            for item in invoice.items.all().select_related('invoice'):
                item.set_rates(rates)
                result.append(item)

        return result

    def get_invoice_totals(self, items):
        return {
            'qty': sum([i.qty for i in items]),
            'wholesale_total': sum([i.wholesale_subtotal_uah for i in items]),
            'retail_total': sum([i.subtotal_with_discount for i in items]),
            'discounted_retail_total': sum(
                [i.discounted_subtotal for i in items]),
            'profit_total': sum([i.profit_subtotal_uah for i in items])
        }

    def handle_product_change(self, product):
        self._handle_product_stock_change(product)

    def _handle_product_stock_change(self, product):

        difference = product.stock - product.initial_stock

        if not difference:
            return

        if difference > 0:
            self._create_arrival_for_product(product, difference)
        else:
            self._create_write_off_for_product(product, abs(difference))

    def _create_arrival_for_product(self, product, qty):

        arrival = self._get_todays_invoice(Arrival, Arrival.TYPE_INCOME)

        arrival.add_item(product, qty=qty, update_product=False)

    def _create_write_off_for_product(self, product, qty):

        sale = self._get_todays_invoice(Sale, Sale.TYPE_WRITE_OFF)

        sale.add_item(product, qty=qty, update_product=False)

    def _get_todays_invoice(self, model, invoice_type):

        today = timezone.now().date()
        today_min = timezone.make_aware(datetime.combine(today, time.min))
        today_max = timezone.make_aware(datetime.combine(today, time.max))

        params = {
            'creator': self._user,
            'type': invoice_type
        }

        try:
            return model.objects.filter(
                created__range=(today_min, today_max), **params)[0]
        except IndexError:
            return model.objects.create(**params)

    def _get_invoice_model(self, invoice_type):

        models = {
            'sale': Sale,
            'arrival': Arrival
        }

        try:
            return models[invoice_type]
        except KeyError:
            raise Exception('Unknown invoice type: {}'.format(invoice_type))

    def _check_access(self):
        if not self._user.is_staff:
            raise Exception(_('Access denied'))


@register_service('invoices')
def _construct_service(services, user, **kwargs):
    return InvoicesService(user)
