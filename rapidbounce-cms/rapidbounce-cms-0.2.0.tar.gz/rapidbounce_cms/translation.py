from modeltranslation.translator import translator, TranslationOptions
from .models import *


class PageTranslationOptions(TranslationOptions):
    fields = (
        "menu",
        "extra_menu",
        "friendlyurl",
        "external_url",
    )


class ContentTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "small_title",
        "description",
    )


class SeoTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )


class ImageDetailsTranslationOptions(TranslationOptions):
    fields = ("title", "alt", "caption_big", "caption_small")


class SocialTagsTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )


class SocialTranslationOptions(TranslationOptions):
    fields = ("url",)


class CompanyDetailsTranslationOptions(TranslationOptions):
    fields = (
        "address",
        "location",
        "country",
    )


class AwardTranslationOptions(TranslationOptions):
    fields = ("url",)


class AwardImageTranslationOptions(TranslationOptions):
    fields = ("image",)


translator.register(Page, PageTranslationOptions)
translator.register(Content, ContentTranslationOptions)
translator.register(Seo, SeoTranslationOptions)
translator.register(ImageDetails, ImageDetailsTranslationOptions)
translator.register(SocialTags, SocialTagsTranslationOptions)
translator.register(Social, SocialTranslationOptions)
translator.register(CompanyDetails, CompanyDetailsTranslationOptions)
translator.register(Award, AwardTranslationOptions)
translator.register(AwardImage, AwardImageTranslationOptions)
