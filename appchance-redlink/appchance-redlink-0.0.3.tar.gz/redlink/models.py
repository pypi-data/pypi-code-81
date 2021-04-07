import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from django_extensions.db.models import TimeStampedModel
from redlink import app_settings
from redlink.redlink_client import (
    ActionType,
    ReceiverDict,
    ReceiverType,
    RedlinkClient,
)
from redlink.utils import chunk_queryset

User = get_user_model()


class RedlinkClientMixin:
    _redlink_client = None

    @property
    def redlink_client(self) -> RedlinkClient:
        if self._redlink_client is None:
            self._redlink_client = RedlinkClient(settings.REDLINK_API_KEY)
        return self._redlink_client


class RedlinkDeviceQuerySet(RedlinkClientMixin, models.QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model=model, query=query, using=using, hints=hints)
        self.CHUNK_SIZE = app_settings.REDLINK_BATCH_SIZE
        self.DEFAULT_LANGUAGE = app_settings.REDLINK_DEFAULT_LANGUAGE

    def user_devices(self, user):
        return self.filter(user=user, active=True)

    def with_marketing_consent(self):
        return self.filter(active=True, settings__marketing=True)

    def with_transactional_consent(self):
        return self.filter(actrive=True, settings__transactional=True)

    def send_push(self, title, body, external_data=None, language=None, **kwargs):
        for registration_ids_chunk in chunk_queryset(
            self.filter(active=True).values("pk", "registration_id"),
            chunk_size=self.CHUNK_SIZE,
        ):
            receivers = [
                ReceiverDict(
                    {
                        "receiver": device["registration_id"],
                        "type": ReceiverType.DEVICE_RECEIVER,
                    }
                )
                for device in registration_ids_chunk
            ]
            if language is None:
                language = self.DEFAULT_LANGUAGE

            if receivers:
                self.redlink_client.send_push(
                    applications=settings.REDLINK_APPLICATIONS,
                    to=receivers,
                    title={language: title},
                    body={language: body},
                    external_data=external_data,
                    action_type=ActionType.WEBVIEW.value,
                    default_language=language,
                    **kwargs
                )


class AbstractRedlinkDevice(RedlinkClientMixin, models.Model):
    DEVICE_TYPES = (
        (u"ios", u"ios"),
        (u"android", u"android"),
    )
    id = models.UUIDField(
        primary_key=True,
        verbose_name="Device ID",
        blank=False,
        unique=True,
        help_text="Unique device identifier",
        max_length=150,
        default=uuid.uuid4,
    )
    registration_id = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="redlink_devices",
    )

    name = models.CharField(max_length=255, verbose_name="Name", null=True)
    active = models.BooleanField(default=True)
    type = models.CharField(choices=DEVICE_TYPES, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RedlinkDeviceQuerySet.as_manager()

    class Meta:
        abstract = True

    def send_push(
        self, title: str, body: str, external_data=None, language=None, **kwargs
    ):
        if language is None:
            language = self.redlink_client.DEFAULT_LANGUAGE
        self.redlink_client.send_push(
            applications=settings.REDLINK_APPLICATIONS,
            to=[
                ReceiverDict(
                    {
                        "receiver": self.registration_id,
                        "type": ReceiverType.DEVICE_RECEIVER,
                    }
                )
            ],
            title={language: title},
            body={language: body},
            external_data=external_data,
            action_type=ActionType.WEBVIEW.value,
            default_language=language,
            **kwargs
        )


class AbstractSentPush(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications", null=True
    )
    content = models.IntegerField()
    is_read = models.BooleanField(default=False)

    class Meta:
        abstract = True
