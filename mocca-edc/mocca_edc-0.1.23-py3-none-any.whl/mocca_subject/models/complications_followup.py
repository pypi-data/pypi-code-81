from edc_model import models as edc_models
from respond_models.mixins import ComplicationsFollowupMixin

from ..model_mixins import CrfModelMixin


class ComplicationsFollowup(
    ComplicationsFollowupMixin, CrfModelMixin, edc_models.BaseUuidModel
):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Complications: Followup"
        verbose_name_plural = "Complications: Followup"
