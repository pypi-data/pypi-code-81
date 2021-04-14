from edc_model import models as edc_models
from respond_models.mixins import PHQ9ModelMixin

from ..model_mixins import CrfModelMixin


class PatientHealth(PHQ9ModelMixin, CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(PHQ9ModelMixin.Meta, CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
