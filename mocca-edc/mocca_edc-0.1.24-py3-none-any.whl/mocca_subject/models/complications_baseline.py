from edc_model import models as edc_models
from respond_models.mixins import ComplicationsBaselineModelMixin

from ..model_mixins import CrfModelMixin


class ComplicationsBaseline(
    ComplicationsBaselineModelMixin, CrfModelMixin, edc_models.BaseUuidModel
):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Complications: Baseline"
        verbose_name_plural = "Complications: Baseline"
