import pdb

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django_audit_fields.admin import ModelAdminAuditFieldsMixin, audit_fieldset_tuple
from edc_constants.constants import DEAD, NO, YES
from edc_dashboard import url_names
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    TemplatesModelAdminMixin,
)
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin
from edc_sites import get_current_country

from mocca_screening.models.model_mixins import CareModelMixin

from ..admin_site import mocca_screening_admin
from ..forms import MoccaRegisterContactForm, MoccaRegisterForm
from ..mocca_original_sites import get_mocca_sites_by_country
from ..models import (
    CareStatus,
    MoccaRegister,
    MoccaRegisterContact,
    SubjectRefusal,
    SubjectRefusalScreening,
    SubjectScreening,
)
from .list_filters import CallListFilter, ContactAttemptsListFilter, ScreenedListFilter


class MoccaRegisterContactInlineMixin:
    model = MoccaRegisterContact
    form = MoccaRegisterContactForm
    extra = 0
    readonly_fields = ["report_datetime"]
    radio_fields = {
        "answered": admin.VERTICAL,
        "respondent": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
        "willing_to_attend": admin.VERTICAL,
        "icc": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }


class AddMoccaRegisterContactInline(
    ModelAdminAuditFieldsMixin, MoccaRegisterContactInlineMixin, admin.StackedInline
):
    fieldsets = (
        [None, {"fields": ("report_datetime",)}],
        (
            "Details of the call",
            {
                "fields": (
                    "answered",
                    "respondent",
                    "survival_status",
                    "death_date",
                    "willing_to_attend",
                    "icc",
                    "next_appt_date",
                    "call_again",
                    "comment",
                ),
            },
        ),
    )
    verbose_name = "New Contact Attempt"
    verbose_name_plural = "New Contact Attempt"

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        return MoccaRegisterContact.objects.none()


class ViewMoccaRegisterContactInline(
    ModelAdminAuditFieldsMixin, MoccaRegisterContactInlineMixin, admin.StackedInline
):

    fieldsets = (
        [None, {"fields": (("report_datetime", "answered"),)}],
        (
            "Details of the call",
            {
                "classes": ("collapse",),
                "fields": (
                    "respondent",
                    "survival_status",
                    "death_date",
                    "willing_to_attend",
                    "icc",
                    "next_appt_date",
                    "call_again",
                    "comment",
                ),
            },
        ),
    )
    verbose_name = "Past Contact Attempt"
    verbose_name_plural = "Past Contact Attempts"

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(MoccaRegister, site=mocca_screening_admin)
class MoccaRegisterAdmin(
    TemplatesModelAdminMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminFormInstructionsMixin,
    SimpleHistoryAdmin,
):
    form = MoccaRegisterForm
    inlines = [AddMoccaRegisterContactInline, ViewMoccaRegisterContactInline]
    ordering = ["mocca_study_identifier"]
    show_object_tools = True
    list_per_page = 15

    care_status_add_url = "mocca_screening_admin:mocca_screening_carestatus_add"
    care_status_change_url = "mocca_screening_admin:mocca_screening_carestatus_change"
    changelist_url_name = "mocca_screening_admin:mocca_screening_moccaregister_changelist"
    refusal_add_url = "mocca_screening_admin:mocca_screening_subjectrefusalscreening_add"
    refusal_change_url = "mocca_screening_admin:mocca_screening_subjectrefusalscreening_change"
    screening_add_url = "mocca_screening_admin:mocca_screening_subjectscreening_add"
    screening_listboard_url_name = "screening_listboard_url"

    fieldsets = (
        [None, {"fields": ("screening_identifier",)}],
        [
            "Original Enrollment Data",
            {
                "fields": (
                    "mocca_study_identifier",
                    "mocca_screening_identifier",
                    "mocca_site",
                    "first_name",
                    "last_name",
                    "initials",
                    "gender",
                    "dob",
                    "birth_year",
                    "age_in_years",
                )
            },
        ],
        [
            "Contact",
            {
                "fields": (
                    "notes",
                    "tel_one",
                    "tel_two",
                    "tel_three",
                    "best_tel",
                    "screen_now",
                )
            },
        ],
        audit_fieldset_tuple,
    )

    list_display = (
        "mocca_patient",
        "call_now",
        "care_status",
        "refusal",
        "screen",
        "date_last_called",
        "next_appt_date",
        "user_modified",
    )

    list_display_links = ("mocca_patient", "call_now")

    list_filter = (
        ScreenedListFilter,
        ContactAttemptsListFilter,
        CallListFilter,
        "date_last_called",
        "next_appt_date",
        "gender",
        "created",
        "modified",
    )

    radio_fields = {
        "best_tel": admin.VERTICAL,
        "call": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "mocca_site": admin.VERTICAL,
        "screen_now": admin.VERTICAL,
    }

    search_fields = (
        "mocca_study_identifier",
        "initials",
        "mocca_screening_identifier",
        "screening_identifier",
        "user_modified",
        "user_created",
    )

    def call_now(self, obj):
        return f"{obj.call} ({obj.contact_attempts})"

    call_now.admin_order_field = "call"

    def mocca_patient(self, obj):
        return str(obj)

    mocca_patient.admin_order_field = "mocca_study_identifier"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=None)
        fields = [
            "contact_attempts",
            "screening_identifier",
            "mocca_study_identifier",
            "mocca_screening_identifier",
            "mocca_site",
        ]
        readonly_fields = list(readonly_fields)
        for f in fields:
            if f not in readonly_fields:
                readonly_fields.append(f)
        readonly_fields = tuple(readonly_fields)
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mocca_site":
            sites = get_mocca_sites_by_country(country=get_current_country())
            kwargs["queryset"] = db_field.related_model.objects.filter(
                name__in=[v.name for v in sites.values()]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @staticmethod
    def get_mocca_register(obj):
        return MoccaRegisterContact.objects.get(mocca_register=obj)

    def screen(self, obj=None):
        mocca_register_contact = self.get_mocca_register(obj)
        try:
            subject_refusal_screening = SubjectRefusalScreening.objects.get(mocca_register=obj)
        except ObjectDoesNotExist:
            subject_refusal_screening = None
        if (
            (obj.call == YES and obj.screen_now == NO)
            or mocca_register_contact.survival_status == DEAD
            or subject_refusal_screening
        ):
            return self.get_empty_value_display()
        elif obj.screening_identifier:
            url = reverse(
                url_names.get(self.screening_listboard_url_name),
                kwargs=self.get_screening_listboard_url_kwargs(obj),
            )
            # url = f"{url}?mocca_register={str(obj.id)}"
            label = obj.screening_identifier
            fa_icon = "fas fa-share"
            fa_icon_after = True
            button_type = "go"
        else:
            add_url = reverse(self.screening_add_url)
            url = f"{add_url}?next={self.changelist_url_name}&mocca_register={str(obj.id)}"
            try:
                care_status = CareStatus.objects.get(mocca_register=obj)
            except ObjectDoesNotExist:
                pass
            else:
                care_status_query_string = "&".join(
                    [
                        f"{f}={getattr(care_status, f) or ''}"
                        for f in [f.name for f in CareModelMixin._meta.fields]
                    ]
                )
                url = f"{url}&{care_status_query_string}"
            label = "Add"
            fa_icon = "fas fa-plus"
            fa_icon_after = None
            button_type = "add"
        context = dict(
            title=f"{SubjectScreening._meta.verbose_name}",
            url=url,
            label=label,
            fa_icon=fa_icon,
            fa_icon_after=fa_icon_after,
            button_type=button_type,
        )
        return render_to_string(self.button_template, context=context)

    def get_screening_listboard_url_name(self):
        return url_names.get(self.screening_listboard_url_name)

    @staticmethod
    def get_screening_listboard_url_kwargs(obj):
        return dict(screening_identifier=obj.screening_identifier)

    @property
    def button_template(self):
        return "mocca_screening/bootstrap3/dashboard_button.html"

    def is_deceased(self, obj=None):
        return getattr(self.get_last_contact(obj), "survival_status", "") == DEAD

    def care_status(self, obj=None):
        """Returns an url to Add/Edit the CareStatus
        or the empty_value string.
        """
        if (
            not self.called_once(obj)
            or self.get_subject_screening_obj(obj=obj)
            or self.is_deceased(obj)
        ):
            return "deceased" if self.is_deceased(obj) else self.get_empty_value_display()
        try:
            care_status = CareStatus.objects.get(mocca_register=obj)
        except ObjectDoesNotExist:
            url = reverse(self.care_status_add_url)
            url = f"{url}?next={self.changelist_url_name}" f"&mocca_register={str(obj.id)}"
            label = "Add"
            fa_icon = "fas fa-plus"
        else:
            url = reverse(self.care_status_change_url, args=(care_status.id,))
            url = f"{url}?next={self.changelist_url_name}"
            label = "Edit"
            fa_icon = "fas fa-pen"
        context = dict(
            title=f"{CareStatus._meta.verbose_name}",
            url=url,
            label=label,
            fa_icon=fa_icon,
            button_type="add" if label == "Add" else "edit",
        )
        return render_to_string(self.button_template, context=context)

    care_status.short_description = "Care Status"

    def refusal(self, obj=None):
        """Returns an url to Add/Edit the SubjectRefusalScreening
        or the empty_value string.
        """
        mocca_register_contact = self.get_mocca_register(obj)
        if (
            not self.called_once(obj)
            or self.get_subject_screening_obj(obj=obj)
            or mocca_register_contact.survival_status == DEAD
        ):
            return self.get_empty_value_display()
        try:
            subject_refusal_screening = SubjectRefusalScreening.objects.get(mocca_register=obj)
        except ObjectDoesNotExist:
            url = reverse(self.refusal_add_url)
            url = f"{url}?next={self.changelist_url_name}&mocca_register={str(obj.id)}"
            label = "Add"
            fa_icon = "fas fa-plus"
        else:
            url = reverse(self.refusal_change_url, args=(subject_refusal_screening.id,))
            url = f"{url}?next={self.changelist_url_name}"
            label = "Edit"
            fa_icon = "fas fa-pen"
        context = dict(
            title=f"{SubjectRefusalScreening._meta.verbose_name}",
            url=url,
            label=label,
            fa_icon=fa_icon,
            button_type="add" if label == "Add" else "edit",
        )
        return render_to_string(self.button_template, context=context)

    @staticmethod
    def get_subject_screening_obj(obj=None):
        try:
            return SubjectScreening.objects.get(mocca_register=obj)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def called_once(obj=None):
        return MoccaRegisterContact.objects.filter(mocca_register=obj).exists()

    @staticmethod
    def get_last_contact(obj=None):
        return (
            MoccaRegisterContact.objects.filter(mocca_register=obj).order_by("-created").last()
        )
