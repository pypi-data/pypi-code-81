from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models
from respond_models.mixins import GlucoseModelMixin

from ..model_mixins import CrfModelMixin


class Glucose(GlucoseModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    glucose_performed = models.CharField(
        verbose_name=(
            "Has the patient had their glucose measured today or since the last visit?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Glucose: Followup"
        verbose_name_plural = "Glucose: Followup"


class GlucoseBaseline(Glucose):
    class Meta:
        proxy = True
        verbose_name = "Glucose: Baseline"
        verbose_name_plural = "Glucose: Baseline"
