from datetime import date, datetime
from typing import Type

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from edc_constants.constants import YES
from edc_visit_schedule.constants import DAY1


def is_baseline(subject_visit):
    return (
        subject_visit.appointment.visit_code == DAY1
        and subject_visit.appointment.visit_code_sequence == 0
    )


def get_clinical_review_baseline_model_cls() -> Type[models.Model]:
    return django_apps.get_model(f"{settings.SUBJECT_APP_LABEL}.clinicalreviewbaseline")


def get_clinical_review_model_cls() -> Type[models.Model]:
    return django_apps.get_model(f"{settings.SUBJECT_APP_LABEL}.clinicalreview")


def get_medication_model_cls() -> Type[models.Model]:
    return django_apps.get_model(f"{settings.SUBJECT_APP_LABEL}.medications")


def get_initial_review_model_cls(prefix) -> Type[models.Model]:
    return django_apps.get_model(f"{settings.SUBJECT_APP_LABEL}.{prefix.lower()}initialreview")


def get_review_model_cls(prefix) -> Type[models.Model]:
    return django_apps.get_model(f"{settings.SUBJECT_APP_LABEL}.{prefix.lower()}review")


def art_initiation_date(subject_identifier: str, report_datetime: datetime) -> date:
    """Returns date initiated on ART or None"""
    art_date = None
    try:
        initial_review = get_initial_review_model_cls("hiv").objects.get(
            subject_visit__subject_identifier=subject_identifier,
            report_datetime__lte=report_datetime,
        )
    except ObjectDoesNotExist:
        pass
    else:
        if initial_review.arv_initiated == YES:
            art_date = initial_review.best_art_initiation_date
        else:
            for review in (
                get_initial_review_model_cls("hiv")
                .objects.filter(
                    subject_visit__subject_identifier=subject_identifier,
                    report_datetime__lte=report_datetime,
                )
                .order_by("-report_datetime")
            ):
                if review.arv_initiated == YES:
                    art_date = review.arv_initiation_actual_date
                    break
    return art_date
