from django.db import models
from django.db.models.query import QuerySet
from scarlet.versioning.models import Cloneable, VersionView
from scarlet.versioning.fields import FKToVersion
from scarlet.pagebuilder import settings, base_models

"""
This file can be copied into a project's app folder as models.py for
default implementation of Pagebuilder.
"""


class Page(VersionView, base_models.BasePage):
    _clone_related = [
        "hero_modules",
        "two_column_modules",
        "icon_list_modules",
        "header_modules",
        "faq_modules",
        "location_modules",
        "gallery_modules",
        "carousel_modules",
    ]
    versioned_unique = ("slug",)

    @property
    def site_name(self):
        return settings.SITE_NAME


class HeroModule(Cloneable, base_models.BaseHeroModule):
    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="hero_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    styles = (("left", "left"), ("right", "right"), ("center", "center"))
    behaviors = (("horizontal", "horizontal"), ("vertical", "vertical"))


class TwoColumnModule(Cloneable, base_models.BaseTwoColumnModule):
    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="two_column_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )


class IconListManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("icon_list_items")


class IconListModule(Cloneable, base_models.BaseIconListModule):
    _clone_related = ("icon_list_items",)
    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="icon_list_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    objects = IconListManager()

    @property
    def items(self) -> QuerySet:
        return self.icon_list_items.all()


class IconListItem(Cloneable, base_models.BaseIconListItem):
    module = models.ForeignKey(
        settings.ICON_LIST_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="icon_list_items",
    )


class HeaderModule(Cloneable, base_models.BaseHeaderModule):
    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="header_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    styles = (("left", "left"), ("right", "right"), ("center", "center"))
    behaviors = (("horizontal", "horizontal"), ("vertical", "vertical"))


class FAQManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("faq_items")


class FAQModule(Cloneable, base_models.BaseFAQModule):
    _clone_related = ("faq_items",)
    objects = FAQManager()

    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="faq_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def items(self) -> QuerySet:
        return self.faq_items.all()


class FAQItem(Cloneable, base_models.BaseFAQItem):
    module = models.ForeignKey(
        settings.FAQ_MODULE_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="faq_items",
    )


class LocationManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("location_items")


class LocationModule(Cloneable, base_models.BaseLocationModule):
    _clone_related = ("location_items",)
    objects = LocationManager()

    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="location_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def items(self) -> QuerySet:
        return self.location_items.all()


class LocationItem(Cloneable, base_models.BaseLocationItem):
    module = models.ForeignKey(
        settings.LOCATION_MODULE_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="location_items",
    )


class GalleryManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("gallery_images")


class ImageGalleryModule(Cloneable, base_models.BaseImageGalleryModule):
    _clone_related = ("gallery_images",)
    objects = GalleryManager()

    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="gallery_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def items(self) -> QuerySet:
        return self.gallery_images.all()


class GalleryImage(Cloneable, base_models.BaseGalleryImage):
    module = models.ForeignKey(
        settings.GALLERY_MODULE_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="gallery_images",
    )


class CarouselManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("carousel_items")


class CarouselModule(Cloneable, base_models.BaseCarouselModule):
    _clone_related = ("carousel_items",)
    objects = CarouselManager()

    @property
    def items(self) -> QuerySet:
        return self.carousel_items.all()

    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="carousel_modules",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )


class CarouselItem(Cloneable, base_models.BaseCarouselItem):
    module = models.ForeignKey(
        settings.CAROUSEL_MODULE_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="carousel_items",
    )
