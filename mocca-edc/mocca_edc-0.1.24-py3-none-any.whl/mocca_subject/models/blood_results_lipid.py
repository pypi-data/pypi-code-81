from edc_crf.model_mixins import CrfNoManagerModelMixin
from edc_model import models as edc_models
from edc_reportable.model_mixin import BloodResultsModelMixin
from respond_models.mixins.blood_results import BloodResultsLipidModelMixin


class BloodResultsLipid(
    BloodResultsLipidModelMixin,
    CrfNoManagerModelMixin,
    BloodResultsModelMixin,
    edc_models.BaseUuidModel,
):
    reportables_name = "mocca"

    class Meta(CrfNoManagerModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Result: Lipids"
        verbose_name_plural = "Blood Results: Lipids"
