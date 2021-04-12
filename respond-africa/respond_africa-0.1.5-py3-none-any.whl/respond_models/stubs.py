from datetime import date, datetime
from typing import List, Protocol, Union

from django.db import models
from edc_crf.stubs import MetaModelStub
from edc_list_data.stubs import ListModelMixinStub
from edc_model import models as edc_models
from edc_visit_tracking.stubs import SubjectVisitModelStub


class ClinicalReviewBaselineModelStub(Protocol):
    subject_visit: SubjectVisitModelStub
    report_datetime: Union[datetime, models.DateTimeField]
    dm_dx: models.CharField
    dm_test_ago: edc_models.DurationYMDField
    dm_test_date: models.DateField
    dm_test_estimated_date: models.DateTimeField
    hiv_dx: models.CharField
    hiv_test_ago: edc_models.DurationYMDField
    hiv_test_date: models.DateField
    hiv_test_estimated_date: models.DateTimeField
    htn_dx: models.CharField
    htn_test_ago: edc_models.DurationYMDField
    htn_test_date: models.DateField
    htn_test_estimated_date: models.DateTimeField

    site: models.Manager
    history: models.Manager
    objects: models.Manager
    _meta: MetaModelStub


class ClinicalReviewModelStub(Protocol):
    diagnoses_labels: dict
    subject_visit: SubjectVisitModelStub
    report_datetime: Union[datetime, models.DateTimeField]
    dm_dx: models.CharField
    dm_test_date: models.DateField
    dm_test_estimated_date: models.DateTimeField
    hiv_dx: models.CharField
    hiv_test_date: models.DateField
    hiv_test_estimated_date: models.DateTimeField
    htn_dx: models.CharField
    htn_test_date: models.DateField
    htn_test_estimated_date: models.DateTimeField

    site: models.Manager
    history: models.Manager
    objects: models.Manager
    _meta: MetaModelStub


class InitialReviewModelStub(Protocol):
    subject_visit: SubjectVisitModelStub
    report_datetime: Union[datetime, models.DateTimeField]
    dx_ago: str
    dx_date: date
    dx_estimated_date: date
    dx_date_estimated: str

    site: models.Manager
    history: models.Manager
    objects: models.Manager
    _meta: MetaModelStub

    def get_best_dx_date(self) -> Union[date, datetime]:
        ...


class NcdInitialReviewModelStub(Protocol):
    ncd_condition_label: str
    subject_visit: SubjectVisitModelStub
    report_datetime: Union[datetime, models.DateTimeField]
    dx_ago: str
    dx_date: date
    dx_estimated_date: date
    dx_date_estimated: str
    med_start_ago: str
    med_start_estimated_date: date
    med_start_date_estimated: str

    site: models.Manager
    history: models.Manager
    objects: models.Manager
    _meta: MetaModelStub


class DrugSupplyNcdFormMixinStub(Protocol):
    cleaned_data: dict
    data: dict
    list_model_cls: ListModelMixinStub

    def clean(self) -> dict:
        ...

    def raise_on_duplicates(self) -> list:
        ...

    @staticmethod
    def raise_on_missing_drug(rx_names: List[str], inline_drug_names: List[str]) -> list:
        ...
