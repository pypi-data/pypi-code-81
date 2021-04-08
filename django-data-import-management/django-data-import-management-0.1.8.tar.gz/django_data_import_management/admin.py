from django import forms
from django.contrib import admin, messages
from django.contrib.messages.api import success
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django_changelist_toolbar_admin.admin import DjangoChangelistToolbarAdmin
from django_object_toolbar_admin.admin import DjangoObjectToolbarAdmin

from .models import (DJANGO_DATA_IMPORT_WORKFLOWS, DjangoDataImportCase,
                     DjangoDataImportItem,
                     get_django_data_import_workflow_choices)


def django_data_import_do_parse(modeladmin, request, queryset):
    for case in queryset.all():
        try:
            case.do_parse()
            modeladmin.message_user(request, _("Parse data file of case {case} success.").format(case=case.title), messages.SUCCESS)
        except Exception as error:
            modeladmin.message_user(request, _("Parse data file of case {case} failed: {message}").format(case=case.title, message=str(error)), messages.ERROR)
django_data_import_do_parse.short_description = _("Parse selected data files.")


def django_data_import_do_import(modeladmin, request, queryset):
    for case in queryset.all():
        try:
            items = case.do_import()
            ok = 0
            failed = 0
            for item in items:
                if item.success:
                    ok += 1
                else:
                    failed += 1
            modeladmin.message_user(request, _("Import data file of case {case} done, {ok} items success, {failed} items failed.").format(case=case.title, ok=ok, failed=failed), messages.SUCCESS)
        except Exception as error:
            modeladmin.message_user(request, _("Import data file of case {case} failed: {message}").format(case=case.title, message=str(error)), messages.ERROR)
django_data_import_do_import.short_description = _("Import selected data files.")

def django_data_import_do_item_import(modeladmin, request, queryset):
    success_count = 0
    failed_count = 0
    for item in queryset.prefetch_related("case").all():
        try:
            success = item.do_import()
            if success:
                success_count += 1
            else:
                failed_count += 1
        except Exception as error:
            modeladmin.message_user(request, _("Import item {item} failed: {message}").format(item=item.pk, messages=str(error)), messages.ERROR)
            failed_count += 1

    if success_count:
        modeladmin.message_user(request, _("{success} items successfully imported.").format(success=success_count), messages.SUCCESS)
    if failed_count:
        modeladmin.message_user(request, _("{failed} items import failed.").format(failed=failed_count), messages.ERROR)
django_data_import_do_item_import.short_description = _("Import selected items.")

class DjangoDataImportCaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['import_workflow'] = forms.ChoiceField(
            choices=get_django_data_import_workflow_choices(),
            label=_("Import Workflow"),
        )

    class Meta:
        model = DjangoDataImportCase
        fields = "__all__"

class DjangoDataImportCaseAdmin(DjangoObjectToolbarAdmin, admin.ModelAdmin):
    form = DjangoDataImportCaseForm
    list_display = ["title", "import_workflow_display", "parse_result", "import_result", "django_object_toolbar"]
    list_filter = ["import_workflow"]
    actions = [
        django_data_import_do_parse,
        django_data_import_do_import,
    ]
    fieldsets = [
        (_("Import Settings"), {
            "fields": ["title", "import_workflow", "datafile"],
            "classes": ["django-data-import-case-admin-import-settings"],
        }),
        (_("Parse Resslt"), {
            "fields": ["parse_result", "parse_time", "parse_error"],
            "classes": ["django-data-import-case-admin-parse-result"],
        }),
        (_("Import Result"), {
            "fields": ["import_result", "import_time", "import_error"],
            "classes": ["django-data-import-case-admin-import-result"],
        })
    ]
    readonly_fields = ["parse_result", "parse_time", "parse_error", "import_result", "import_time", "import_error"]

    def import_workflow_display(self, obj):
        info = DJANGO_DATA_IMPORT_WORKFLOWS.get(obj.import_workflow, None)
        if info:
            return info["name"]
        else:
            return "-"
    import_workflow_display.short_description = _("Import Workflow")
    import_workflow_display.admin_order_field = "import_workflow"

    django_object_toolbar_buttons = [
        "do_parse",
        "do_import",
        "show_items",
    ]

    def do_parse(self, obj):
        return "#"
    do_parse.icon = "fas fa-book"
    do_parse.title = _("Parse Case")

    def do_import(self, obj):
        return "#"
    do_import.icon = "fas fa-upload"
    do_import.title = _("Import Case")

    def show_items(self, obj):
        return reverse("admin:django_data_import_management_djangodataimportitem_changelist") + "?case__id__exact=" + str(obj.pk)
    show_items.icon = "fas fa-list"
    show_items.title = _("Show Items")

class DjangoDataImportItemAdmin(DjangoChangelistToolbarAdmin, admin.ModelAdmin):
    list_display = ["id", "success", "info", "import_success", "case"]
    list_filter = ["case", "success", "import_success"]
    search_fields = ["info", "json_data"]
    actions = [
        django_data_import_do_item_import,
    ]
    readonly_fields = ["case", "success", "info", "add_time", "json_data", "import_success", "import_time", "import_error"]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("case")

    django_changelist_toolbar_buttons = [
        "show_cases",
    ]

    def show_cases(self, request):
        return reverse("admin:django_data_import_management_djangodataimportcase_changelist")
    show_cases.icon = "fa fa-list"
    show_cases.title = _("Goto Case Changelist")

admin.site.register(DjangoDataImportCase, DjangoDataImportCaseAdmin)
admin.site.register(DjangoDataImportItem, DjangoDataImportItemAdmin)
