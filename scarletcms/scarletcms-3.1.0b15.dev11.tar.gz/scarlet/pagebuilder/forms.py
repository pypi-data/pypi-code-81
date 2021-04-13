from django import forms
from django.forms.models import inlineformset_factory
from scarlet.cms.forms import LazyFormSetFactory
from .settings import (
    MODULE_TYPES,
    HERO_MODULE,
    HEADER_MODULE,
    FAQ_MODULE,
    TWO_COLUMN_MODULE,
    ICON_LIST_MODULE,
    LOCATION_MODULE,
    GALLERY_MODULE,
    CAROUSEL_MODULE,
)
from . import (
    get_page_model,
    get_hero_model,
    get_two_column_model,
    get_icon_list_model,
    get_icon_item_model,
    get_header_model,
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


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = (
            "title",
            "slug",
            "internal_name",
        )


class EmptyPageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = (
            "title",
            "slug",
            "description",
            "keywords",
            "og_image",
            "og_image_alt_text",
        )


class HeroModuleForm(forms.ModelForm):
    class Meta:
        model = HeroModule
        fields = "__all__"


class TwoColumnModuleForm(forms.ModelForm):
    class Meta:
        model = TwoColumnModule
        fields = "__all__"


class HeaderModuleForm(forms.ModelForm):
    class Meta:
        model = HeaderModule
        fields = "__all__"


class IconListModuleForm(forms.ModelForm):
    class Meta:
        model = IconListModule
        fields = "__all__"


class IconListItemForm(forms.ModelForm):
    class Meta:
        model = IconListItem
        fields = "__all__"


class FAQModuleForm(forms.ModelForm):
    class Meta:
        model = FAQModule
        fields = "__all__"


class FAQItemForm(forms.ModelForm):
    class Meta:
        model = FAQItem
        fields = "__all__"


class LocationModuleForm(forms.ModelForm):
    class Meta:
        model = LocationModule
        fields = "__all__"


class LocationItemForm(forms.ModelForm):
    class Meta:
        model = LocationItem
        fields = "__all__"


class ImageGalleryModuleForm(forms.ModelForm):
    class Meta:
        model = ImageGalleryModule
        fields = "__all__"


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = "__all__"


class CarouselModuleForm(forms.ModelForm):
    class Meta:
        model = CarouselModule
        fields = "__all__"


class CarouselItemForm(forms.ModelForm):
    class Meta:
        model = CarouselItem
        fields = "__all__"


class HeroInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(HeroInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            HeroModule,
            can_order=False,
            can_delete=True,
            form=HeroModuleForm,
            fk_name="page",
        )


class TwoColumnInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(TwoColumnInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            TwoColumnModule,
            can_order=False,
            can_delete=True,
            form=TwoColumnModuleForm,
            fk_name="page",
        )


class IconListInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(IconListInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            IconListModule,
            can_order=False,
            can_delete=True,
            form=IconListModuleForm,
            fk_name="page",
        )


class IconItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(IconItemInlineFormset, self).__init__(
            inlineformset_factory,
            IconListModule,
            IconListItem,
            can_order=False,
            can_delete=True,
            form=IconListItemForm,
            fk_name="module",
        )


class HeaderInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(HeaderInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            HeaderModule,
            can_order=False,
            can_delete=True,
            form=HeaderModuleForm,
            fk_name="page",
        )


class FAQInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(FAQInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            FAQModule,
            can_order=False,
            can_delete=True,
            form=FAQModuleForm,
            fk_name="page",
        )


class FAQItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(FAQItemInlineFormset, self).__init__(
            inlineformset_factory,
            FAQModule,
            FAQItem,
            can_order=False,
            can_delete=True,
            form=FAQItemForm,
            fk_name="module",
        )


class LocationInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(LocationInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            LocationModule,
            can_order=False,
            can_delete=True,
            form=LocationModuleForm,
            fk_name="page",
        )


class LocationItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(LocationItemInlineFormset, self).__init__(
            inlineformset_factory,
            LocationModule,
            LocationItem,
            can_order=False,
            can_delete=True,
            form=LocationItemForm,
            fk_name="module",
        )


class ImageGalleryInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(ImageGalleryInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            ImageGalleryModule,
            can_order=False,
            can_delete=True,
            form=ImageGalleryModuleForm,
            fk_name="page",
        )


class GalleryImageInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(GalleryImageInlineFormset, self).__init__(
            inlineformset_factory,
            ImageGalleryModule,
            GalleryImage,
            can_order=False,
            can_delete=True,
            form=GalleryImageForm,
            fk_name="module",
        )


class CarouselInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(CarouselInlineFormset, self).__init__(
            inlineformset_factory,
            Page,
            CarouselModule,
            can_order=False,
            can_delete=True,
            form=CarouselModuleForm,
            fk_name="page",
        )


class CarouselItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(CarouselItemInlineFormset, self).__init__(
            inlineformset_factory,
            CarouselModule,
            CarouselItem,
            can_order=False,
            can_delete=True,
            form=CarouselItemForm,
            fk_name="module",
        )


PAGE_EDIT_FIELDSET = (("Content Modules", {"fields": (),}),)

PAGE_EDIT_FORMSETS = {
    HERO_MODULE: HeroInlineFormset(),
    TWO_COLUMN_MODULE: TwoColumnInlineFormset(),
    HEADER_MODULE: HeaderInlineFormset(),
    ICON_LIST_MODULE: IconListInlineFormset(),
    FAQ_MODULE: FAQInlineFormset(),
    LOCATION_MODULE: LocationInlineFormset(),
    GALLERY_MODULE: ImageGalleryInlineFormset(),
    CAROUSEL_MODULE: CarouselInlineFormset(),
}

MODULE_COMBINED_FORMSET = {
    "title": "Modules",
    "keys": MODULE_TYPES,
}
