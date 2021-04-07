from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.text import slugify
from django import template

register = template.Library()


class FaqPluginModel(CMSPlugin):
    title = models.CharField(_("Title"), max_length=300)

    class Meta:
        verbose_name = _("Faq Container")

    def __unicode__(self):
        try:
            return f"Faq Container − {self.title} − {self.placeholder.page}"
        except AttributeError:
            return f"Faq Container − {self.title} − " + _("Draft")

    def __str__(self):
        try:
            return f"Faq Container − {self.title} − {self.placeholder.page}"
        except AttributeError:
            return f"Faq Container − {self.title} − " + _("Draft")


class QuestionFaqPluginModel(CMSPlugin):
    question = models.CharField(_("Question"), max_length=300)
    keywords = models.ManyToManyField("djangocms_faq.keyword", verbose_name=_("Keywords"))
    slug = models.SlugField(
        blank=True,
        default='',
        help_text=_("Unique slug for this question. Keep empty to let it be auto-generated."),
        max_length=300,
    )

    @property
    def get_full_url(self):
        try:
            return self.page.get_absolute_url()
        except AttributeError:
            return ""

    def copy_relations(self, oldinstance):
        self.keywords.set(oldinstance.keywords.all())

    class Meta:
        verbose_name = _("Faq Question")

    def __unicode__(self):
        return f"Faq Question − {self.question}"


    def save(self, **kwargs):
        if self.slug == "":
            self.slug = slugify(self.question)
        super().save(**kwargs)

class Keyword(models.Model):
    keyword = models.CharField(_("Keyword"), max_length=100)

    def __unicode__(self):
        return f"{self.keyword}"

    def __str__(self):
        return f"{self.keyword}"


class SearchFaqPluginModel(CMSPlugin):
    name = models.CharField(_("Search name"), max_length=50)
    search_in = models.ManyToManyField("djangocms_faq.faqpluginmodel", verbose_name=_("Search in"), limit_choices_to={'placeholder__page__publisher_is_draft': False})

    def get_faq_published_instances():
        return djangocms_faq.FaqPluginModel.objects.all().filter(placeholder__page__publisher_is_draft=True)

    def copy_relations(self, oldinstance):
        self.search_in.set(oldinstance.search_in.all())

    class Meta:
        verbose_name = _("Faq Search")

    def __unicode__(self):
        return f"Faq Search − {self.name}"
