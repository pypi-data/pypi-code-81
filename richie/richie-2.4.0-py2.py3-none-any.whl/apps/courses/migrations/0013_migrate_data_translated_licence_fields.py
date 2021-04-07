# Generated by Django 2.2.8 on 2020-01-02 13:56

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def forwards_func(apps, schema_editor):
    Licence = apps.get_model("courses", "Licence")
    LicenceTranslation = apps.get_model("courses", "LicenceTranslation")

    for licence in Licence.objects.all():
        LicenceTranslation.objects.create(
            master_id=licence.pk,
            language_code=settings.LANGUAGE_CODE,
            name=licence.name_deprecated,
        )


def backwards_func(apps, schema_editor):
    Licence = apps.get_model("courses", "Licence")
    LicenceTranslation = apps.get_model("courses", "LicenceTranslation")

    for licence in Licence.objects.all():
        translation = _get_translation(licence, LicenceTranslation)
        licence.name_deprecated = translation.name
        licence.save()  # Note this only calls Model.save()


def _get_translation(licence, LicenceTranslation):
    translations = LicenceTranslation.objects.filter(master_id=licence.pk)
    try:
        # Try default translation
        return translations.get(language_code=settings.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        try:
            # Try default language
            return translations.get(language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE)
        except ObjectDoesNotExist:
            # Maybe the object was translated only in a specific language?
            # Take the first existing translation
            return translations.first()


class Migration(migrations.Migration):

    dependencies = [("courses", "0012_add_translation_model_for_licence_fields")]

    operations = [migrations.RunPython(forwards_func, backwards_func)]
