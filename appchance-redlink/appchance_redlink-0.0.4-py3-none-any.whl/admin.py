from django.contrib import admin

from redlink.models import RedlinkDevice, SentPush


class RedlinkDeviceAdminAbstract:
    list_display = (
        "id",
        "registration_id",
        "user",
        "name",
        "type",
        "created",
        "updated",
    )
    readonly_fields = ("user",)
    search_fields = ("id", "registration_id", "user__id")


@admin.register(RedlinkDevice)
class RedlinkDeviceAdmin(RedlinkDeviceAdminAbstract, admin.ModelAdmin):
    pass


@admin.register(SentPush)
class SentPushAdmin(admin.ModelAdmin):
    pass
