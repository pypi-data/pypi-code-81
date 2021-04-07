from django.contrib import admin

from .models import PopupPluginModel


class DjangocmsPopupAdmin(admin.ModelAdmin):
    list_display = ("id", "get_page_url", "display_delay", "can_reopen_popup")

    def get_queryset(self, request):
        print(super(DjangocmsPopupAdmin, self).get_queryset(request))
        qs = (
            super(DjangocmsPopupAdmin, self)
            .get_queryset(request)
            .exclude(placeholder__page__publisher_is_draft=True)
        )
        return qs


admin.site.register(PopupPluginModel, DjangocmsPopupAdmin)
