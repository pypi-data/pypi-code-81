from time import timezone

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


from django_simpletask.models import SimpleTask
from django_safe_fields.fields import SafeCharField
from django_safe_fields.fields import SafeTextField


class WaringCategory(models.Model):
    code = models.CharField(max_length=255, unique=True, verbose_name=_("Warning Category Code"))
    name = models.CharField(max_length=255, verbose_name=_("Warning Category Name"))
    display_order = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Warning Category")
        verbose_name_plural = _("Warning Categories")

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, code):
        try:
            return cls.objects.get(code=code)
        except cls.DoesNotExist:
            return None


class Warning(SimpleTask):
    category = models.ForeignKey(WaringCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Warning Category"))
    title = SafeCharField(max_length=256, verbose_name=_("Warning Title"))
    data = SafeTextField(null=True, blank=True, verbose_name=_("Warning Data"))
    ack = models.BooleanField(default=False, verbose_name=_("Acknowledged"))
    ack_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Acknowledged Time"))

    class Meta:
        verbose_name = _("Warning")
        verbose_name_plural = _("Warnings")

    def __str__(self):
        return self.title

    @classmethod
    def make(cls, category, title, data=None, save=False):
        category = WaringCategory.get(category)
        try:
            instance = cls.objects.get(ack=False, category=category, title=title)
            return None
        except cls.DoesNotExist:
            instance = cls()
            instance.category = category
            instance.title = title
            instance.data = data
            if save:
                instance.save()
            return instance

    @classmethod
    def makemany(cls, category, warnings, save=False):
        warning_instances = []
        for warning in warnings:
            if isinstance(warning, (list, tuple)):
                data = warning[1]
                warning = warning[0]
            else:
                data = None
            instance = Warning.make(category, warning, data=data, save=False)
            if instance:
                instance.ready(save=False)
                warning_instances.append(instance)
        if save:
            Warning.objects.bulk_create(warning_instances)
        return warning_instances

    def acknowledge(self, save=True):
        self.ack = True
        self.ack_time = timezone.now()
        if save:
            self.save()
        