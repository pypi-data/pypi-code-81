from django.contrib import admin


class CompletionFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '数据集分类'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'filter'

    def lookups(self, request, model_admin):

        return (
            ('lt1', ('待补录数据')),
            ('eq1', ('完整数据')),
            ('all', ('全部数据'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'lt1':
            return queryset.filter(data_completion__lt=1).order_by('id')
        elif self.value() == 'eq1':
            return queryset.filter(data_completion=1).order_by('id')
        elif self.value() == 'all':
            return queryset.order_by('id')
        else:
            return queryset.order_by('id')
