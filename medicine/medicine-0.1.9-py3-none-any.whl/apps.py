from DjangoAppCenter.extensions.apps.permission_init import PermissionInitMixin
from django.apps import AppConfig


class MedicineConfig(AppConfig, PermissionInitMixin):
    name = 'medicine'
    verbose_name = "药品"

    models_path = "medicine.models"
    base_orm_models = ("SnowFlakeIdentifiedModel", "MetaBasic")

    def ready(self):
        PermissionInitMixin.ready(self)
