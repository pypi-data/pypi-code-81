from rest_framework.viewsets import ModelViewSet

from .mixins import PermissionFilterMixin

__all__ = ["PermissionFilterModelViewSet"]


class PermissionFilterModelViewSet(PermissionFilterMixin, ModelViewSet):
    pass
