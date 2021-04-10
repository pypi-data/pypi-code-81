from django.urls import path

from NEMO_billing import views

urlpatterns = [
    path("custom_charges/", views.custom_charges, name="custom_charges"),
    path("custom_charge/", views.create_or_modify_custom_charge, name="create_custom_charge"),
    path("custom_charge/<int:custom_charge_id>", views.create_or_modify_custom_charge, name="edit_custom_charge"),
]
