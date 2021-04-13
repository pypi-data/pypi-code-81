import warnings

__all__ = ["PermissionFilter", "PermissionFilterGroup"]


class PermissionFilter:
    permission_id = None

    def trigger_filter(self, filter_name, *args, **kwargs):
        selected_filter = getattr(self, filter_name)
        return selected_filter(*args, **kwargs)

    def get_allowed_actions(self, request, view, obj=None):
        """Return container of allowed actions.

        Defaults to list of all ViewSet actions.

        By default PermissionFilterMixin calls this method during `ViewSet.initialize` with `obj=None`,
        and during `ViewSet.check_object_permissions` with `obj=something`.

        Should NOT return `None`.

        """
        actions = getattr(view, "action_map", {}) or {}
        actions = list(actions.values())
        actions = actions or ["create", "list", "retrieve",
                              "update", "partial_update", "destroy"]
        return actions

    def get_queryset(self, request, view, queryset):
        """Return modified queryset for this permission, or None if no modifications required."""
        return

    def get_serializer_class(self, request, view):
        """Return modified serializer class for this permission, or None if no modifications required."""
        return

    def get_serializer(self, request, view, serializer_class, *args, **kwargs):
        """Return modified serializer instance for this permission, or None if no modifications required."""
        return


class PermissionFilterGroup:
    def __init__(self, permission_filters):
        self.permission_filters = {}

        for permission_filter in permission_filters:
            if(isinstance(permission_filter.permission_id, list)):
                for permission_id in permission_filter.permission_id:
                    self.permission_filters[permission_id] = permission_filter
            else:
                self.permission_filters[permission_filter.permission_id] = permission_filter
                #self.permission_filters = {permission_filter.permission_id: permission_filter for permission_filter in permission_filters}

    def get_permission_filter(self, permission_id):
        filter = next(
            (x for x in permission_id if self.permission_filters.get(x)), None)
        return self.permission_filters.get(filter)

    def trigger_filter(self, filter_name, permission_id, *args, **kwargs):
        permission_filter = self.get_permission_filter(permission_id)
        if permission_filter is None:
            return
        return permission_filter.trigger_filter(filter_name, *args, **kwargs)

    def get_allowed_actions(self, permission_id, request, view, obj=None):
        try:
            allowed_actions = self.trigger_filter(
                "get_allowed_actions", permission_id, request, view, obj=obj)
        except TypeError:
            allowed_actions = self.trigger_filter(
                "get_allowed_actions", permission_id, request, view)
            warnings.warn(
                "PermissionFilter.get_allowed_actions without support for `obj` argument is deprecated",
                PendingDeprecationWarning,
            )

        if allowed_actions is None:
            return []
        return allowed_actions

    def get_queryset(self, permission_id, request, view, queryset):
        return self.trigger_filter("get_queryset", permission_id, request, view, queryset)

    def get_serializer_class(self, permission_id, request, view):
        return self.trigger_filter("get_serializer_class", permission_id, request, view)

    def get_serializer(self, permission_id, request, view, serializer_class, *args, **kwargs):
        return self.trigger_filter(
            "get_serializer", permission_id, request, view, serializer_class, *args, **kwargs
        )
