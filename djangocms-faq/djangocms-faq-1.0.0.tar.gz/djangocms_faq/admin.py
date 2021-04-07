from django.contrib import admin

from .models import Keyword


class DjangocmsFaqKeywordAdmin(admin.ModelAdmin):

    list_display = ("id", "keyword")
    search_field = ("keyword")

    fieldsets = (
        ("Add a keyword", {
            "fields": ("keyword",)
        }),
    )




admin.site.register(
    Keyword, DjangocmsFaqKeywordAdmin
)
