from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Warning
from .models import WaringCategory

from .actions import django_site_warnings_acknowledge

class WaringCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
    ordering = ["display_order"]

class WarningAdmin(admin.ModelAdmin):
    list_display = ["title", "add_time", "warning_status", "ack"]
    list_filter = ["category", "status", "ack"]
    readonly_fields = [] + Warning.SIMPLE_TASK_FIELDS

    def warning_status(self, obj):
        return obj.get_status_display()
    warning_status.short_description = _("Warning Status")

    actions = [
        django_site_warnings_acknowledge,
    ]

    
admin.site.register(WaringCategory, WaringCategoryAdmin)
admin.site.register(Warning, WarningAdmin)
