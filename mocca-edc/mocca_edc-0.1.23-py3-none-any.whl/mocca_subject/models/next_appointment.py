from django.db import models
from edc_model import models as edc_models
from edc_model.models import date_is_future, date_is_not_now

from ..model_mixins import CrfModelMixin


class NextAppointment(CrfModelMixin, edc_models.BaseUuidModel):

    appt_date = models.DateField(
        verbose_name="Next scheduled routine appointment",
        validators=[date_is_not_now, date_is_future],
        null=True,
        blank=True,
        help_text="if applicable.",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Routine Appointment"
        verbose_name_plural = "Routine Appointments"
