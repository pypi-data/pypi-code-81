from django.conf import settings

from djoptimizely.utils.helpers import get_func_from_str


def _get_user_id(request):
    user_id_func = get_func_from_str(settings.OPTIMIZELY_USER_ID)
    return user_id_func(request)

def _get_user_attribs(request):
    user_attrib_func = get_func_from_str(settings.OPTIMIZELY_USER_ATTRIBS)
    return user_attrib_func(request)

def get_feature_enabled(request, flag_key):
    enabled = False
    if hasattr(request, 'optimizely_client'):
        client = request.optimizely_client.get_client()
        if client:
            user_id = _get_user_id(request)
            attributes = _get_user_attribs(request)
            enabled = client.is_feature_enabled(flag_key, user_id, attributes)
    return enabled
