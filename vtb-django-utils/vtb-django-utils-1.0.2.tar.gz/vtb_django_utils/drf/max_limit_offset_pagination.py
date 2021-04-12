from collections import OrderedDict

from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class MaxLimitOffsetPagination(PageNumberPagination):
    """
        Include in settings.py:
        REST_FRAMEWORK = {
            'DEFAULT_PAGINATION_CLASS': 'core.drf.max_limit_offset_pagination.MaxLimitOffsetPagination',
            'MAX_PAGE_SIZE': int(os.environ.get('MAX_PAGE_SIZE', '100')),
            ...
            }
    """
    page_query_param = 'page'
    page_query_description = _('Page number')

    page_size_query_param = 'per_page'
    page_size_query_description = _('Number of items per page')

    max_page_size = settings.REST_FRAMEWORK['MAX_PAGE_SIZE']

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('meta', {
                'total_count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }),
            ('list', data)
        ]))
