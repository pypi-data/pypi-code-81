from django.db import models
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import ResizeToFill, SmartResize, ResizeToFit
from datetime import date
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.template import defaultfilters
from mptt.models import MPTTModel, TreeForeignKey
from filer.fields.image import FilerImageField
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.urls import reverse
from django.core.cache import cache
from django.conf import settings

# Clear Cache on save or delete


class CCOnSaveModel(models.Model):
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        cache.clear()
        super(CCOnSaveModel, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        cache.clear()
        super(CCOnSaveModel, self).save(*args, **kwargs)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class OrderingModel(models.Model):
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True


class LanguageManager(models.Manager):
    def lang_filter(self, lang):
        return (
            super(LanguageManager, self).get_queryset().filter(language__lang_code=lang)
        )

    def get_page_lang(self, lang):
        return (
            super(LanguageManager, self)
            .get_queryset()
            .filter(language__lang_code=lang)
            .order_by("tree_id", "level", "order")
        )


class Language(TimeStampedModel, OrderingModel, CCOnSaveModel):
    name = models.CharField(max_length=200)
    lang_code = models.CharField(max_length=2)
    display_lang = models.CharField(max_length=2)
    is_default = models.BooleanField(default=False)
    active = models.BooleanField(db_index=True, default=False)

    def get_absolute_url(self):  # For Sitemap
        return "/" + self.lang_code + "/"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class Page(MPTTModel, TimeStampedModel, OrderingModel):
    name = models.CharField(db_index=True, max_length=200)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        on_delete=models.CASCADE,
    )
    menu = models.CharField(max_length=200, default="")
    extra_menu = models.CharField(max_length=200, default="", null=True, blank=True)
    friendlyurl = models.SlugField(
        db_index=True, max_length=300, default="", null=True, blank=True
    )
    external_url = models.CharField(max_length=255, default="", null=True, blank=True)
    page_class = models.CharField(max_length=255, default="", null=True, blank=True)
    show = models.BooleanField(db_index=True, default=True)
    # Models Manager
    # objects =       LanguageManager()

    # Auto Slug only on create
    def save(self, *args, **kwargs):
        if not self.id:
            # self.friendlyurl = defaultfilters.slugify(unidecode(self.menu))
            self.friendlyurl_en = defaultfilters.slugify(unidecode(self.menu_en))
            self.friendlyurl_el = defaultfilters.slugify(unidecode(self.menu_el))
        cache.clear()
        super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self):  # For Sitemap
        # list_urls = reverse('regular_page', kwargs={'lang': 'en', 'friendlyurl':self.friendlyurl})
        # return list_urls
        url = "/%s/%s/" % (get_language(), self.friendlyurl)
        page = self
        while page.parent:
            url = "/%s/" % self.friendlyurl
            url = "/%s/%s%s" % (get_language(), page.parent.friendlyurl, url)
            page = page.parent
        return url

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ["order"]

    class Meta:
        ordering = ["tree_id", "level", "order"]


class Content(TimeStampedModel, OrderingModel, CCOnSaveModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    small_title = models.CharField(max_length=200, default="", null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Seo(TimeStampedModel, CCOnSaveModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    # Models Manager
    objects = LanguageManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "SEO"


class Image(CCOnSaveModel):
    content = models.ManyToManyField(Content, blank=True)
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class ImageDetails(TimeStampedModel, CCOnSaveModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    alt = models.CharField(max_length=200, default="")
    caption_big = models.CharField(max_length=200, default="", null=True, blank=True)
    caption_small = models.CharField(max_length=200, default="", null=True, blank=True)
    # Models Manager
    objects = LanguageManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Images Meta Data"


class GoogleJs(TimeStampedModel, CCOnSaveModel):
    tag_manager = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name_plural = "Google Tags"


class SocialTags(TimeStampedModel, CCOnSaveModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=95, default="")
    description = models.TextField(default="")
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    # Models Manager
    objects = LanguageManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Social Tag"
        verbose_name_plural = "Social Tags"


class Social(TimeStampedModel, OrderingModel, CCOnSaveModel):
    name = models.CharField(max_length=200)
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    icon = models.CharField(max_length=200)
    url = models.CharField(max_length=255)
    active = models.BooleanField(db_index=True, default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name = "Social"
        verbose_name_plural = "Socials"


class Contact(TimeStampedModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    comments = models.TextField()
    referral = models.TextField(null=True, blank=True, default=settings.WEBSITENAME)
    ipaddress = models.CharField(max_length=20, null=True, blank=True)
    user_agent = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name


class Review(TimeStampedModel):
    name = models.CharField(max_length=200, default="Anonymous")
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    review = models.TextField()
    publish = models.BooleanField(default=False)
    source = models.CharField(max_length=200, default=settings.WEBSITENAME)
    date = models.DateField(editable=True, null=False, default=date.today)
    visited = models.DateField(editable=True, null=True, blank=True)
    stars = models.IntegerField(default=5)
    order = models.IntegerField(default=0, null=True, blank=True)
    referral = models.TextField(null=True, blank=True)
    ipaddress = models.CharField(max_length=20, null=True, blank=True)
    user_agent = models.CharField(max_length=200, null=True, blank=True)
    copy_email = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.name


class CompanyDetails(TimeStampedModel, CCOnSaveModel):
    logo_main = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    logo_secondary = FilerImageField(
        null=True, blank=True, related_name="logo_secondary", on_delete=models.CASCADE
    )
    bkeng_url = models.CharField(max_length=200, null=True, blank=True)
    echeckin_url = models.CharField(max_length=200, null=True, blank=True)
    telephone_code = models.CharField(max_length=200, null=True, blank=True)
    telephone1 = models.CharField(max_length=200, null=True, blank=True)
    telephone2 = models.CharField(max_length=200, null=True, blank=True)
    telephone3 = models.CharField(max_length=200, null=True, blank=True)
    telephone4 = models.CharField(max_length=200, null=True, blank=True)
    telephone5 = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    fax = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    email2 = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, default="")
    location = models.CharField(max_length=200, default="")
    country = models.CharField(max_length=200, default="", null=True, blank=True)
    gmaps_latitude = models.CharField(max_length=200, null=True, blank=True)
    gmaps_longitude = models.CharField(max_length=200, null=True, blank=True)
    gps_latitude = models.CharField(max_length=200, null=True, blank=True)
    gps_longitude = models.CharField(max_length=200, null=True, blank=True)
    tbrn = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Company Details"

    def __str__(self):
        return "Company Details"


class Award(TimeStampedModel, OrderingModel, CCOnSaveModel):
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Awards"

    def __str__(self):
        return self.name


class AwardImage(TimeStampedModel, OrderingModel, CCOnSaveModel):
    award = models.ForeignKey(Award, related_name="images", on_delete=models.CASCADE)
    image = FilerImageField(on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Award Images"

    def __str__(self):
        return self.award.name


class Subscribe(TimeStampedModel):
    email = models.EmailField(
        unique=True,
        error_messages={"unique": _("This email has already been registered.")},
    )
    referral = models.TextField(null=True, blank=True, default=settings.WEBSITENAME)
    ipaddress = models.CharField(max_length=20, null=True, blank=True)
    user_agent = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return self.email


class Offers(TimeStampedModel):
    name = models.CharField(max_length=200)
    image = ProcessedImageField(
        upload_to="photos/special_offers/",
        processors=[ResizeToFill(1000, 600, False)],
        format="JPEG",
        options={"quality": 95},
    )
    offer_start = models.DateTimeField()
    offer_end = models.DateTimeField()
    url = models.CharField(max_length=200)
    active = models.BooleanField(db_index=True, default=True)

    def save(self, *args, **kwargs):
        if self.active:
            try:
                tmp = Offers.objects.get(active=True)
                if self != tmp:
                    tmp.active = False
                    tmp.save()
            except Offers.DoesNotExist:
                pass
        cache.clear()
        super(Offers, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Special Offer"
        verbose_name_plural = "Special Offers"