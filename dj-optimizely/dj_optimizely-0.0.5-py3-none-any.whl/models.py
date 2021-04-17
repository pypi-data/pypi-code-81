from django.db import models
from django.utils.translation import ugettext_lazy as _


class OptimizelyDataFile(models.Model):
    environment = models.CharField(max_length=255, unique=True)
    current_revision = models.IntegerField(null=True, blank=True)
    json = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
