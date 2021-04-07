from django.contrib import admin
from import_export import resources

from .models import EmailSchedule

class EmailScheduleResource(resources.ModelResource):
    class Meta:
        model = EmailSchedule

class EmailScheduleAdmin(admin.ModelAdmin):
    resource_class = EmailScheduleResource

admin.site.register(EmailSchedule, EmailScheduleAdmin)
