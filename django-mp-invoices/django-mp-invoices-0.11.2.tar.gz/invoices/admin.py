
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cap.decorators import template_list_item, short_description

from invoices.models import Arrival, Sale


@admin.register(Arrival, Sale)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = [
        'get_name',
        'type',
        'customer',
        'creator',
        'get_total_qty',
        'get_total',
        'get_item_actions'
    ]
    list_display_links = ['type']
    list_filter = ['type', 'creator', 'created', 'customer']
    search_fields = ['id']

    def has_add_permission(self, request):
        return False

    @template_list_item('invoices/name_cell.html', _('Created'))
    def get_name(self, obj):
        return {'object': obj}

    @short_description(_('Total'))
    def get_total(self, obj):
        return obj.total

    @short_description(_('Total qty'))
    def get_total_qty(self, obj):
        return obj.total_qty

    @template_list_item('invoices/list_item_actions.html', _('Actions'))
    def get_item_actions(self, obj):
        return {'object': obj}
