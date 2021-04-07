from django.shortcuts import get_object_or_404

from redlink.models import RedlinkDevice
from redlink.serializers import (
    RedlinkCreateDeviceSerializer,
    RedlinkDeviceSerializer,
)
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class RedlinkDeviceViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = RedlinkDeviceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "registration_id"

    def get_serializer_class(self):
        if self.action == "create":
            return RedlinkCreateDeviceSerializer
        return RedlinkDeviceSerializer

    def get_queryset(self):
        return RedlinkDevice.objects.filter(active=True, user=self.request.user)

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, registration_id=self.kwargs["registration_id"])

    def perform_create(self, serializer):
        device = serializer.save(user=self.request.user)
        self._deactivate_devices_with_equal_registration_id(device=device)
        return device

    def perform_update(self, serializer):
        device = serializer.save(user=self.request.user, session_key="")
        if "registration_id" in serializer.initial_data:
            self._deactivate_devices_with_equal_registration_id(device=device)
        return device

    def _deactivate_devices_with_equal_registration_id(self, device):
        RedlinkDevice.objects.filter(registration_id=device.registration_id,).exclude(
            id=device.id
        ).update(active=False)
