from .models import Account

from django_filters.rest_framework import DjangoFilterBackend


class FilterBackend(DjangoFilterBackend):
    def get_filterset(self, request, queryset, view):
        fs = super().get_filterset(request, queryset, view)
        for name, field in fs.form.fields.items():
            if not hasattr(field, 'queryset'):
                continue
            if field.queryset.model == Account:
                if not request.user.is_authenticated:
                    field.queryset = field.queryset.none()
                elif not request.user.is_superuser:
                    field.queryset = field.queryset.for_user(request.user)
        return fs
