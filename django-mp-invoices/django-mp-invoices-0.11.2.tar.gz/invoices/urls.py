
from django.urls import path

from invoices import views

app_name = 'invoices'


urlpatterns = [

    path('<str:invoice_type>/create/',
         views.create_invoice,
         name='create'),

    path('<str:invoice_type>/<int:invoice_id>/manage/',
         views.manage_invoice,
         name='manage'),

    path('<str:invoice_type>/<int:invoice_id>/print/',
         views.print_invoice,
         name='print'),

    path('<str:invoice_type>/report/',
         views.get_report,
         name='report'),

    path('<str:invoice_type>/<int:invoice_id>/set-customer/',
         views.set_customer,
         name='set-customer'),

    path('<str:invoice_type>/<int:invoice_id>/set-discount/',
         views.set_discount,
         name='set-discount'),

    path('<str:invoice_type>/<int:invoice_id>/add-item/',
         views.add_item,
         name='add-item'),

    path('<str:invoice_type>/<int:invoice_id>/set-item-qty/<int:item_id>/',
         views.set_item_qty,
         name='set-item-qty'),

    path('<str:invoice_type>/<int:invoice_id>/set-item-price/<int:item_id>/',
         views.set_item_price,
         name='set-item-price'),

    path('<str:invoice_type>/<int:invoice_id>/remove-item/<int:item_id>/',
         views.remove_item,
         name='remove-item'),

    path('add-product/',
         views.add_product,
         name='add-product'),

    path('add-customer/',
         views.add_customer,
         name='add-customer'),

    path('products/', views.get_products, name='products')

]
