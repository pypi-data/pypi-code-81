from datetime import date

from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import MALE
from edc_crf.model_mixins import (
    CrfModelMixin,
    CrfNoManagerModelMixin,
    CrfWithActionModelMixin,
)
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_lab.model_mixins import PanelModelMixin
from edc_list_data.model_mixins import ListModelMixin
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_model import models as edc_models
from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_reference.model_mixins import (
    ReferenceModelMixin,
    RequisitionReferenceModelMixin,
)
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_reportable.model_mixin import BloodResultsModelMixin
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_schedule.model_mixins import OffScheduleModelMixin, OnScheduleModelMixin
from edc_visit_tracking.model_mixins import (
    SubjectVisitMissedModelMixin,
    VisitModelMixin,
)

from respond_models.mixins import (
    ClinicalReviewBaselineCholModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineModelMixin,
    ClinicalReviewModelMixin,
    FastingGlucoseModelMixin,
    FastingModelMixin,
    GlucoseModelMixin,
    HivArvInitiationModelMixin,
    HivArvMonitoringModelMixin,
    InitialReviewModelMixin,
    OgttModelMixin,
)
from respond_models.mixins.clinical_review.clinical_review import (
    ClinicalReviewCholModelMixin,
    ClinicalReviewDmModelMixin,
    ClinicalReviewHivModelMixin,
    ClinicalReviewHtnModelMixin,
)
from respond_models.mixins.medication import (
    CholMedicationsModelMixin,
    DmMedicationsModelMixin,
    HivMedicationsModelMixin,
    HtnMedicationsModelMixin,
)


class OnSchedule(OnScheduleModelMixin, edc_models.BaseUuidModel):
    class Meta(edc_models.BaseUuidModel.Meta):
        pass


class OffSchedule(
    OffScheduleModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        pass


class SubjectOffstudy(
    OffstudyModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(OffstudyModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass


class DeathReport(
    UniqueSubjectIdentifierFieldMixin,
    edc_models.BaseUuidModel,
):

    objects = SubjectIdentifierManager()

    def natural_key(self):
        return tuple(
            self.subject_identifier,
        )


class SubjectConsent(
    UniqueSubjectIdentifierFieldMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    edc_models.BaseUuidModel,
):

    consent_datetime = models.DateTimeField(default=get_utcnow)

    version = models.CharField(max_length=25, default="1")

    identity = models.CharField(max_length=25, default="111111111")

    confirm_identity = models.CharField(max_length=25, default="111111111")

    dob = models.DateField(default=date(1995, 1, 1))

    gender = models.CharField(max_length=25, default=MALE)

    objects = SubjectIdentifierManager()

    def natural_key(self):
        return tuple(
            self.subject_identifier,
        )


class SubjectVisit(
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    edc_models.BaseUuidModel,
):

    subject_identifier = models.CharField(max_length=50)

    reason = models.CharField(max_length=25)

    class Meta(edc_models.BaseUuidModel.Meta):
        pass


class SubjectRequisition(
    CrfModelMixin,
    RequisitionReferenceModelMixin,
    PanelModelMixin,
    UpdatesRequisitionMetadataModelMixin,
    edc_models.BaseUuidModel,
):

    requisition_datetime = models.DateTimeField(null=True)

    is_drawn = models.CharField(max_length=25, choices=YES_NO, null=True)

    reason_not_drawn = models.CharField(max_length=25, null=True)

    class Meta(edc_models.BaseUuidModel.Meta):
        pass


class CrfOne(CrfModelMixin, edc_models.BaseUuidModel):

    f1 = models.CharField(max_length=50, null=True)

    f2 = models.CharField(max_length=50, null=True)

    f3 = models.CharField(max_length=50, null=True)

    class Meta(edc_models.BaseUuidModel.Meta):
        pass


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    edc_models.BaseUuidModel,
):

    action_identifier = models.CharField(max_length=50, null=True)

    tracking_identifier = models.CharField(max_length=30, null=True)

    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="+"
    )

    class Meta(
        SubjectVisitMissedModelMixin.Meta,
        edc_models.BaseUuidModel.Meta,
    ):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"


class TestCrfModelMixin(CrfModelMixin):
    class Meta:
        abstract = True


class TestCrfNoManagerModelMixin(CrfNoManagerModelMixin):
    class Meta:
        abstract = True


class ReasonsForTesting(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Reasons for Testing"
        verbose_name_plural = "Reasons for Testing"


class ClinicalReview(
    ClinicalReviewHivModelMixin,
    ClinicalReviewHtnModelMixin,
    ClinicalReviewDmModelMixin,
    ClinicalReviewCholModelMixin,
    ClinicalReviewModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(
        ClinicalReviewModelMixin.Meta,
        CrfModelMixin.Meta,
        edc_models.BaseUuidModel.Meta,
    ):
        pass


class ClinicalReviewBaseline(
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineCholModelMixin,
    ClinicalReviewBaselineModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(
        ClinicalReviewBaselineModelMixin.Meta,
        CrfModelMixin.Meta,
        edc_models.BaseUuidModel.Meta,
    ):
        pass


class HivInitialReview(
    HivArvInitiationModelMixin,
    HivArvMonitoringModelMixin,
    InitialReviewModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "HIV Initial Review"


class DmInitialReview(
    InitialReviewModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Diabetes Initial Review"


class HtnInitialReview(
    InitialReviewModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Hypertension Initial Review"


class CholInitialReview(
    InitialReviewModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Cholesterol Initial Review"


class HivReview(
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "HIV Review"


class DmReview(
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Diabetes Review"


class HtnReview(
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Hypertension Review"


class CholReview(
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Cholesterol Review"


class Medications(
    HivMedicationsModelMixin,
    HtnMedicationsModelMixin,
    DmMedicationsModelMixin,
    CholMedicationsModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Medications"
        verbose_name_plural = "Medications"


class GlucoseResult(
    GlucoseModelMixin,
    BloodResultsModelMixin,
    TestCrfNoManagerModelMixin,
    edc_models.BaseUuidModel,
):

    glucose_performed = models.CharField(
        verbose_name=(
            "Has the patient had their glucose measured today or since the last visit?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    class Meta(TestCrfNoManagerModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Glucose"
        verbose_name_plural = "Glucose"


class GlucoseAssessment(
    FastingModelMixin,
    FastingGlucoseModelMixin,
    OgttModelMixin,
    TestCrfModelMixin,
    edc_models.BaseUuidModel,
):

    ifg_performed = models.CharField(
        verbose_name="Was the IFG test performed?",
        max_length=15,
        choices=YES_NO,
    )

    ifg_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    ogtt_performed = models.CharField(
        verbose_name="Was the OGTT test performed?",
        max_length=15,
        choices=YES_NO,
    )

    ogtt_not_performed_reason = models.CharField(
        verbose_name="If NO, provide reason", max_length=150, null=True, blank=True
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Glucose (IFG, OGTT)"
        verbose_name_plural = "Glucose (IFG, OGTT)"


class NonAdherenceReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "NonAdherence Reasons"
        verbose_name_plural = "NonAdherence Reasons"
