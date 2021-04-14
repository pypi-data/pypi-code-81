from datetime import datetime
import pytz

from django.db import models

tz = pytz.timezone('Europe/Stockholm')
current_time = datetime.now(tz=tz)


class Clients(models.Model):
    active = models.BooleanField(verbose_name="Aktiv", blank=False, default=True)
    name = models.CharField(
        max_length=200, verbose_name="Namn", blank=True, default='')
    company = models.CharField(
        max_length=200, verbose_name="Företag", blank=True, default='')
    phone = models.CharField(
        max_length=20, verbose_name="Telefon", blank=True, default='')
    email = models.CharField(
        max_length=100, verbose_name="E-postadress", blank=True, default='')
    org_number = models.CharField(
        max_length=10, verbose_name="Org nummer", blank=True, default='')
    position = models.CharField(
        max_length=100, verbose_name="Title", blank=True, default='')
    selected_client = models.BooleanField(verbose_name="Utvald kund", blank=True, default=False)
    """
    Aggregations
    """
    last_7_days_visits = models.IntegerField(verbose_name="Besök - sista 7 dagar", blank=False, default=0)
    last_30_days_visits = models.IntegerField(verbose_name="Besök - sista 30 dagar", blank=False, default=0)
    all_visits = models.IntegerField(verbose_name="Alla besök", blank=False, default=0)
    last_visit = models.DateTimeField(verbose_name="Sista besök", null=True, blank=True, auto_now=False,
                                      auto_now_add=False)

    uid = models.IntegerField(verbose_name='UID', blank=False, unique=True)
    bot = models.IntegerField(verbose_name='Bot', blank=False, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kund"
        verbose_name_plural = "Kunder"

    def __str__(self):
        return self.email


class ClientHistory(models.Model):
    ACTION_CHOICES = (
        ('RG', 'Telefonsamtal'),
        ('EM', 'Skickat email'),
        ('RE', 'Svar'),
        ('AV', 'Avregistera'),
        ('AN', 'Annat'),
    )
    action = models.CharField(
        max_length=15,
        choices=ACTION_CHOICES,
        default='RG',
        verbose_name='Aktion'
    )
    note = models.TextField(verbose_name="Anteckingar", blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="get_history_for_client", default='')

    class Meta:
        verbose_name = "Historik"
        verbose_name_plural = "Historik"

    def __str__(self):
        return str(self.created)


class Visits(models.Model):
    uid = models.IntegerField(blank=False, verbose_name='uid')
    url = models.CharField(blank=False, verbose_name='URL', max_length=255)
    created_at = models.DateTimeField(verbose_name="Skapat", )

    class Meta:
        verbose_name = "Besökta sidan"
        verbose_name_plural = "Besökta sidor"


class AggVisits(models.Model):
    uid = models.IntegerField(blank=False, verbose_name='uid')
    visits = models.IntegerField(blank=False, default=0)
    date = models.DateTimeField(verbose_name="date", null=True, blank=True)


class Newsletter(models.Model):
    name = models.CharField(max_length=200, verbose_name="Namn", blank=True, default='')
    created_at = models.DateTimeField(verbose_name="Skapad", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class NewsletterLink(models.Model):
    link = models.CharField(max_length=255, verbose_name="Link", blank=True)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name="get_link_for_newsletter")

    def __str__(self):
        return self.link
