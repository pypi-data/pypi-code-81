from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "respond_model"
    verbose_name = "RESPOND-AFRICA model mixins"
    has_exportable_data = False
    include_in_administration_section = False
