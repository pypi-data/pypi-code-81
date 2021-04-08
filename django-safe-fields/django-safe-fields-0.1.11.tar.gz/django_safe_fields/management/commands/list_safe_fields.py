import djclick as click
from django.apps import apps
from django_safe_fields.fields import SafeFieldMixinBase

@click.command()
def list_safe_fields():
    for app_label, models in apps.all_models.items():
        for model_name, model in models.items():
            for field in model._meta.fields:
                if isinstance(field, SafeFieldMixinBase):
                    print("{}\t{}\t{}".format(field.__class__.__name__, field.cipher.__class__.__name__, field))
