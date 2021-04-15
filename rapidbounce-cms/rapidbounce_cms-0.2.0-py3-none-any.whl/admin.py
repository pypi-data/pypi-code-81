from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from django.conf import settings
from reversion.admin import VersionAdmin
from imagekit.admin import AdminThumbnail
from mptt.admin import DraggableMPTTAdmin
from .models import *


@admin.register(CompanyDetails)
class CompanyDetailsAdmin(TranslationAdmin, VersionAdmin):
    pass


@admin.register(Page)
class PageAdmin(TranslationAdmin, VersionAdmin, DraggableMPTTAdmin):
    list_display = [
        "tree_actions",
        "indented_title",
        "name",
        "parent",
        "level",
        "lft",
        "rght",
        "tree_id",
        "menu",
        "friendlyurl",
        "show",
        "order",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["name"]
    list_editable = ["show", "order"]
    list_filter = ["name", "show", "created_at", "updated_at"]
    search_fields = ["name"]


@admin.register(Language)
class LanguageAdmin(VersionAdmin):
    list_display = [
        "name",
        "lang_code",
        "is_default",
        "active",
        "order",
        "created_at",
        "updated_at",
    ]
    list_editable = ["order", "active", "is_default"]


class ImageInline(admin.TabularInline):
    model = Image.content.through
    extra = 1


@admin.register(Content)
class ContentAdmin(TranslationAdmin, VersionAdmin):
    # This option is for creating new object rather than updating the existing
    save_as = True
    # If False we redirect to ChangeList View else we stay at editing page
    save_as_continue = True
    inlines = [
        ImageInline,
    ]
    list_display = [
        "get_page",
        "title",
        "small_title",
        "order",
        "created_at",
        "updated_at",
    ]
    list_filter = ["page__name", "created_at", "updated_at"]
    search_fields = ["page__name"]
    ordering = ("order",)
    list_editable = [
        "order",
    ]

    def get_page(self, obj):
        return obj.page.name

    get_page.short_description = "Page"


class ImageDetailsInline(TranslationTabularInline):
    model = ImageDetails
    extra = 1
    max_num = 1
    # exclude = ['',]


@admin.register(Image)
class ImageAdmin(VersionAdmin):
    inlines = [
        ImageDetailsInline,
    ]
    list_display = [
        "get_content",
        "admin_thumbnail",
        "name",
        "get_title",
        "order",
        "uploaded_at",
    ]
    admin_thumbnail = AdminThumbnail(
        image_field="image", template="admin/thumbnail.html"
    )
    list_editable = [
        "order",
    ]
    ordering = ("order",)  # The negative sign indicate descendent order
    filter_horizontal = ("content",)

    def get_content(self, obj):
        return "\n".join([c.title for c in obj.content.all()])

    def get_title(self, obj):
        title = ",".join([k.title for k in obj.imagedetails_set.all()])
        if title:
            return '<img src="' + settings.STATIC_URL + 'admin/img/icon-yes.svg">'
        else:
            return '<img src="' + settings.STATIC_URL + 'admin/img/icon-no.svg">'

    get_content.short_description = "Content"
    get_title.short_description = "Meta Tags"
    get_title.allow_tags = True

    list_filter = ["content__page", "content__title", "uploaded_at"]
    search_fields = [
        "content__title",
    ]


@admin.register(Seo)
class SeoAdmin(TranslationAdmin, VersionAdmin):
    list_display = ["get_page", "title", "created_at", "updated_at"]
    list_display_links = ["get_page"]
    list_filter = ["page__name", "created_at", "updated_at"]
    search_fields = [
        "page__name",
    ]
    # Geting Foreign Keys
    def get_page(self, obj):
        return obj.page.name

    get_page.short_description = "Page"


class AwardImageInline(TranslationTabularInline):
    model = AwardImage
    extra = 1
    # max_num = 1


@admin.register(Award)
class AwardAdmin(TranslationAdmin, VersionAdmin):
    inlines = [
        AwardImageInline,
    ]
    list_display = ["name"]


@admin.register(SocialTags)
class SocialTagsAdmin(VersionAdmin):
    list_display = ["page"]


@admin.register(Social)
class SocialAdmin(TranslationAdmin, VersionAdmin):
    list_display = ["name"]


@admin.register(GoogleJs)
class GoogleJsAdmin(VersionAdmin):
    list_display = ["tag_manager"]


@admin.register(Review)
class ReviewAdmin(VersionAdmin):
    list_display = [
        "name",
        "email",
        "location",
        "title",
        "stars",
        "date",
        "publish",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["name"]
    list_filter = ["name", "location", "stars", "created_at", "updated_at"]
    search_fields = ["name", "location"]


@admin.register(Contact)
class ContactAdmin(VersionAdmin):
    list_display = ["name"]


@admin.register(Subscribe)
class SubscribeAdmin(VersionAdmin):
    pass