from django.db.models import Manager
from django.conf import settings as dj_settings
from rest_framework import serializers

from .utils import get_image_urls
from . import (
    settings,
    get_page_model,
    get_hero_model,
    get_header_model,
    get_two_column_model,
    get_icon_list_model,
    get_icon_item_model,
    get_faq_model,
    get_faq_item_model,
    get_location_model,
    get_location_item_model,
    get_image_gallery_model,
    get_gallery_item_model,
    get_carousel_model,
    get_carousel_item_model,
)

Page = get_page_model()
HeroModule = get_hero_model()
HeaderModule = get_header_model()
TwoColumnModule = get_two_column_model()
IconListModule = get_icon_list_model()
IconListItem = get_icon_item_model()
FAQModule = get_faq_model()
FAQItem = get_faq_item_model()
LocationModule = get_location_model()
LocationItem = get_location_item_model()
ImageGalleryModule = get_image_gallery_model()
GalleryImage = get_gallery_item_model()
CarouselModule = get_carousel_model()
CarouselItem = get_carousel_item_model()


class HeroModuleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: HeroModule) -> dict:
        images_json = get_image_urls(obj, "image", settings.WIDE_IMAGE_SIZES)
        images_json["altText"] = obj.image_alt_text
        return images_json

    class Meta:
        model = HeroModule
        fields = (
            "kind",
            "image",
            "header",
            "subheader",
            "button_url",
            "button_text",
            "style",
            "behavior",
        )


class TwoColumnModuleSerializer(serializers.ModelSerializer):
    left_image = serializers.SerializerMethodField()
    right_image = serializers.SerializerMethodField()

    def get_left_image(self, obj: TwoColumnModule) -> dict:
        images_json = get_image_urls(obj, "left_image", settings.SQUARE_IMAGE_SIZES)
        images_json["altText"] = obj.left_image_alt_text
        return images_json

    def get_right_image(self, obj: TwoColumnModule) -> dict:
        images_json = get_image_urls(obj, "right_image", settings.SQUARE_IMAGE_SIZES)
        images_json["altText"] = obj.right_image_alt_text
        return images_json

    class Meta:
        model = TwoColumnModule
        fields = (
            "kind",
            "left_image",
            "left_header",
            "left_description",
            "left_button_url",
            "left_button_text",
            "right_image",
            "right_header",
            "right_description",
            "right_button_url",
            "right_button_text",
            "style",
            "behavior",
        )


class HeaderModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderModule
        fields = (
            "kind",
            "header",
            "subheader",
            "style",
            "behavior",
        )


class IconListItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        images_json = get_image_urls(obj, "icon")
        images_json["altText"] = obj.icon_alt_text
        return images_json

    class Meta:
        model = IconListItem
        fields = (
            "kind",
            "icon",
            "text",
        )


class IconListModuleSerializer(serializers.ModelSerializer):
    items = IconListItemSerializer(many=True)

    class Meta:
        model = IconListModule
        fields = (
            "kind",
            "title",
            "subtitle",
            "footnote",
            "items",
            "style",
            "behavior",
        )


class FAQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = (
            "kind",
            "question",
            "answer",
        )


class FAQModuleSerializer(serializers.ModelSerializer):
    items = FAQItemSerializer(many=True)

    class Meta:
        model = FAQModule
        fields = (
            "kind",
            "items",
            "style",
            "behavior",
        )


class LocationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationItem
        fields = (
            "kind",
            "title",
            "address1",
            "address2",
            "city",
            "region",
            "zip_code",
            "country",
            "hours",
            "phone_number",
        )


class LocationModuleSerializer(serializers.ModelSerializer):
    items = LocationItemSerializer(many=True)

    class Meta:
        model = LocationModule
        fields = (
            "kind",
            "items",
            "style",
            "behavior",
        )


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: GalleryImage) -> dict:
        images_json = get_image_urls(obj, "image", settings.GALLERY_IMAGE_SIZES)
        images_json["altText"] = obj.image_alt_text
        return images_json

    class Meta:
        model = GalleryImage
        fields = (
            "kind",
            "image",
        )


class ImageGallerySerializer(serializers.ModelSerializer):
    items = GalleryImageSerializer(many=True)

    class Meta:
        model = ImageGalleryModule
        fields = (
            "kind",
            "items",
            "style",
            "behavior",
        )


class CarouselItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: CarouselItem) -> dict:
        images_json = get_image_urls(obj, "image", settings.CAROUSEL_IMAGE_SIZES)
        images_json["altText"] = obj.image_alt_text
        return images_json

    class Meta:
        model = CarouselItem
        fields = (
            "kind",
            "title",
            "subtitle",
            "image",
            "button_url",
            "button_text",
        )


class CarouselModuleSerializer(serializers.ModelSerializer):
    items = CarouselItemSerializer(many=True)

    class Meta:
        model = CarouselModule
        fields = (
            "kind",
            "button_url",
            "button_text",
            "items",
            "style",
            "behavior",
        )


class PageListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, Manager) else data
        return [self.child.to_representation(item, many=True) for item in iterable]


class PageSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize Page model or any module using flexible module structure.
    Creates response with `head` object as first item in list, followed by all modules
    serialized based on the serializer_map.
    """

    og_image = serializers.SerializerMethodField()

    def get_og_image(self, obj: Page) -> str:
        return get_image_urls(obj, "og_image")

    def _get_modules(self, obj) -> list:
        modules = []
        for module_type in self.Meta.module_fields:
            modules += getattr(obj, module_type).all()
            # TODO: Test if modules.insert() for each in all() is faster than current
        return sorted(modules, key=lambda x: x.order,)

    def _module_to_representation(self, module) -> str:
        return self.Meta.serializer_map.get(type(module))(module).data

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()
        return PageListSerializer(*args, **kwargs)

    def to_representation(self, instance, many=False):
        orig_rep = super().to_representation(instance)

        request = self.context.get("request", None)
        url = request.build_absolute_uri() if request else dj_settings.SITE_URL

        head_module = {
            "kind": "head",
            "locale": orig_rep.get("locale", "en-US"),
            "title": orig_rep.get("title", "Wonderful"),
            "description": orig_rep.get("seo_description", ""),
            "keywords": orig_rep.get("keywords", ""),
            "url": url,
            "gtm": orig_rep.get("gtm", "gtm-Test"),
            "open_graph": {
                "kind": "website",
                "url": url,
                "locale": orig_rep.get("locale", "en-US"),
                "title": orig_rep.get("title", "Wonderful"),
                "description": orig_rep.get("seo_description", ""),
                "image": orig_rep.get("og_image", ""),
                "site_name": orig_rep.get("site_name", "Wonderful"),
                "card": "summary_large_image",
            },
        }

        new_rep = {"content": [head_module]}

        if many:
            body = {}
            for key in self.Meta.body_fields:
                body[key] = orig_rep.get(key)

            new_rep["content"].append(body)
        else:
            modules = self._get_modules(instance)
            for mod in modules:
                new_rep["content"].append(self._module_to_representation(mod))

        return new_rep

    class Meta:
        model = Page
        body_fields = (
            "title",
            "slug",
            "seo_description",
            "keywords",
            "og_image",
            "site_name",
        )
        fields = body_fields
        module_fields = (
            "page_hero_modules",
            "page_two_column_modules",
            "page_icon_list_modules",
            "page_header_modules",
            "page_faq_modules",
            "page_location_modules",
            "page_gallery_modules",
            "page_carousel_modules",
        )
        serializer_map = {
            HeroModule: HeroModuleSerializer,
            TwoColumnModule: TwoColumnModuleSerializer,
            IconListModule: IconListModuleSerializer,
            HeaderModule: HeaderModuleSerializer,
            FAQModule: FAQModuleSerializer,
            LocationModule: LocationModuleSerializer,
            ImageGalleryModule: ImageGallerySerializer,
            CarouselModule: CarouselModuleSerializer,
        }


class ObjectPageSerializer(serializers.ModelSerializer):
    """
    Serializes an object similar to the PageSerializer but without module fields
    or serializer map needed for variable modules. Fields should be registered
    like a standard DRF serializer and added to the meta body_fields.
    """

    og_image = serializers.SerializerMethodField()

    def get_og_image(self, obj: Page) -> str:
        return get_image_urls(obj, "icon")

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()
        return PageListSerializer(*args, **kwargs)

    def to_representation(self, instance, many=False):
        orig_rep = super().to_representation(instance)

        request = self.context.get("request", None)
        url = request.build_absolute_uri() if request else dj_settings.SITE_URL

        head = {
            "kind": "head",
            "locale": orig_rep.get("locale", "en-US"),
            "title": orig_rep.get("title", "Wonderful"),
            "description": orig_rep.get("seo_description", ""),
            "keywords": orig_rep.get("keywords", ""),
            "url": url,
            "gtm": orig_rep.get("gtm", "gtm-Test"),
            "open_graph": {
                "kind": "website",
                "url": url,
                "locale": orig_rep.get("locale", "en-US"),
                "title": orig_rep.get("title", "Wonderful"),
                "description": orig_rep.get("seo_description", ""),
                "image": orig_rep.get("og_image", ""),
                "site_name": orig_rep.get("name", ""),
                "card": "summary_large_image",
            },
        }

        new_rep = {"content": [head]}

        if many:
            body = {}
            for key in self.Meta.body_fields:
                body[key] = orig_rep.get(key)

            new_rep["content"].append(body)
        else:
            for key in self.Meta.body_fields:
                if not orig_rep.get(key):
                    continue

                new_rep["content"].append(
                    {"kind": key, "items": orig_rep.get(key),}
                )

        return new_rep

    class Meta:
        model = Page
        body_fields = (
            "title",
            "slug",
            "description",
            "keywords",
            "og_image",
        )
        fields = body_fields
