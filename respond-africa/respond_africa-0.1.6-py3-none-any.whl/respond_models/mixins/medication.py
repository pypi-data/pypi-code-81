from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE


class HivMedicationsModelMixin(models.Model):
    refill_hiv = models.CharField(
        verbose_name="Is the patient filling / refilling HIV medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for HIV infection."
        ),
    )

    class Meta:
        abstract = True


class HtnMedicationsModelMixin(models.Model):
    refill_htn = models.CharField(
        verbose_name="Is the patient filling / refilling Hypertension medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for Hypertension."
        ),
    )

    class Meta:
        abstract = True


class DmMedicationsModelMixin(models.Model):
    refill_dm = models.CharField(
        verbose_name="Is the patient filling / refilling Diabetes medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for Diabetes."
        ),
    )

    class Meta:
        abstract = True


class CholMedicationsModelMixin(models.Model):
    refill_chol = models.CharField(
        verbose_name="Is the patient filling / refilling Cholesterol medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Select `not applicable` if subject has not "
            "been diagnosed and prescribed medication for Cholesterol."
        ),
    )

    class Meta:
        abstract = True
