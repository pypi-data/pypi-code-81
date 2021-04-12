from django.conf import settings

is_django_cms_installed = 'cms' in settings.INSTALLED_APPS

if is_django_cms_installed:
    import logging

    from cms.admin.pageadmin import PageAdmin
    from django.core.cache import cache
    from cms import signals
    from django.utils.cache import _generate_cache_header_key

    logger = logging.getLogger(__name__)


    def delete_cache_key(sender, obj, operation, request,  **kwargs):
        # Workaround for the cache issue https://github.com/django-cms/django-cms/issues/6975
        try:
            if operation == 'publish_page_translation':
                # In order to get the same cache_key as the user would receive we need to create a WSGIRequest
                # object with empty query string and with page path
                request_custom = request
                request_custom.path = obj.get_absolute_url(kwargs['translation'].language)
                request_custom.META['QUERY_STRING'] = ''
                cache_key = _generate_cache_header_key('', request_custom)
                cache.delete(cache_key)
        except Exception as e:
            logger.exception(f'Error in page publish receiver: {e}')


    signals.post_obj_operation.connect(delete_cache_key, PageAdmin)
