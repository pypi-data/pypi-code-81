from django.contrib.auth.models import Permission
from .permission_filters import PermissionFilterGroup

__all__ = ["PermissionFilterMixin"]


class PermissionFilterMixin:
    permission_filter_classes = None
    permission_filter_group = None
    permission_id = None

    @property
    def permission_filter_group(self):
        return self.get_permission_filter_group()

    def get_permission_id(self, request):
        permissions = [
            x.name for x in Permission.objects.filter(user=request.user)]
        permissions = list(permissions)
        return permissions

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.permission_id = self.get_permission_id(request)
        allowed_actions = self.permission_filter_group.get_allowed_actions(
            self.permission_id, request, self)
        if self.action not in allowed_actions:
            self.permission_denied(
                request, message="action={} not allowed for permission={}".format(
                    self.action, self.permission_id)
            )

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = self.permission_filter_group.get_queryset(
            self.permission_id, self.request, self, queryset)
        if filtered_queryset is None:
            return queryset
        return filtered_queryset

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        filtered_serializer_class = self.permission_filter_group.get_serializer_class(
            self.permission_id, self.request, self
        )
        if filtered_serializer_class is None:
            return serializer_class
        return filtered_serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        filtered_serializer = self.permission_filter_group.get_serializer(
            self.permission_id, self.request, self, serializer_class, *args, **kwargs
        )
        if filtered_serializer is None:
            return serializer_class(*args, **kwargs)
        return filtered_serializer

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        allowed_actions = self.permission_filter_group.get_allowed_actions(
            self.permission_id, request, self, obj=obj)
        if self.action not in allowed_actions:
            self.permission_denied(
                request, message="action={} not allowed for permission={}".format(
                    self.action, self.permission_id)
            )

    def get_permission_filter_group(self):
        return PermissionFilterGroup(permission_filters=self.get_permission_filters())

    def get_permission_filters(self):
        return [permission_filter() for permission_filter in self.permission_filter_classes]
