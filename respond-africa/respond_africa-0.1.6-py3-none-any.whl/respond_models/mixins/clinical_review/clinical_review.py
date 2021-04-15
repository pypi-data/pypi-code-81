from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ...constants import RESPOND_DIAGNOSIS_LABELS
from ...stubs import ClinicalReviewModelStub


class ClinicalReviewModelMixin(models.Model):

    diagnoses_labels = RESPOND_DIAGNOSIS_LABELS

    complications = models.CharField(
        verbose_name="Since last seen, has the patient had any complications",
        max_length=15,
        choices=YES_NO,
        help_text="If Yes, complete the `Complications` CRF",
    )

    def get_best_test_date(self: ClinicalReviewModelStub, prefix: str):
        return getattr(self, f"{prefix}_test_date", None) or getattr(
            self, f"{prefix}_test_estimated_datetime", None
        )

    @property
    def diagnoses(self: ClinicalReviewModelStub) -> dict:
        if not self.diagnoses_labels:
            raise ImproperlyConfigured("Settings attribute RESPOND_DIAGNOSIS_LABELS not set.")
        return {k: getattr(self, f"{k}_dx") for k in self.diagnoses_labels}

    class Meta:
        abstract = True
        verbose_name = "Clinical Review"
        verbose_name_plural = "Clinical Review"


class ClinicalReviewHivModelMixin(models.Model):

    hiv_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for HIV infection?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=mark_safe(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )

    hiv_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    hiv_reason = models.ManyToManyField(
        f"{settings.LIST_MODEL_APP_LABEL}.reasonsfortesting",
        related_name="hiv_test_reason",
        verbose_name="Why was the patient tested for HIV infection?",
        blank=True,
    )

    hiv_reason_other = edc_models.OtherCharField()

    hiv_dx = models.CharField(
        verbose_name=mark_safe(
            "As of today, was the patient <u>newly</u> diagnosed with HIV infection?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True


class ClinicalReviewHtnModelMixin(models.Model):

    htn_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for hypertension?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=mark_safe(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )

    htn_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    htn_reason = models.ManyToManyField(
        f"{settings.LIST_MODEL_APP_LABEL}.reasonsfortesting",
        related_name="htn_test_reason",
        verbose_name="Why was the patient tested for hypertension?",
        blank=True,
    )

    htn_reason_other = edc_models.OtherCharField()

    htn_dx = models.CharField(
        verbose_name=mark_safe(
            "As of today, was the patient <u>newly</u> diagnosed with hypertension?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True


class ClinicalReviewDmModelMixin(models.Model):

    dm_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for diabetes?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=mark_safe(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )

    dm_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    dm_reason = models.ManyToManyField(
        f"{settings.LIST_MODEL_APP_LABEL}.reasonsfortesting",
        related_name="dm_reason",
        verbose_name="Why was the patient tested for diabetes?",
        blank=True,
    )

    dm_reason_other = edc_models.OtherCharField()

    dm_dx = models.CharField(
        verbose_name=mark_safe(
            "As of today, was the patient <u>newly</u> diagnosed with diabetes?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True


class ClinicalReviewCholModelMixin(models.Model):

    chol_test = models.CharField(
        verbose_name="Since last seen, was the patient tested for high cholesterol?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=mark_safe(
            "Note: Select `not applicable` if diagnosis previously reported. <BR>"
            "`Since last seen` includes today.<BR>"
            "If `yes', complete the initial review CRF<BR>"
            "If `not applicable`, complete the review CRF."
        ),
    )
    chol_test_date = models.DateField(
        verbose_name="Date test requested",
        null=True,
        blank=True,
    )

    chol_reason = models.ManyToManyField(
        f"{settings.LIST_MODEL_APP_LABEL}.reasonsfortesting",
        related_name="chol_reason",
        verbose_name="Why was the patient tested for cholesterol?",
        blank=True,
    )

    chol_reason_other = edc_models.OtherCharField()

    chol_dx = models.CharField(
        verbose_name=mark_safe(
            "As of today, was the patient <u>newly</u> diagnosed with high cholesterol?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
