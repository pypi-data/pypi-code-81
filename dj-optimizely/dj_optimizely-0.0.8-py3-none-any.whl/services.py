from djoptimizely.settings import (
    get_user_id_callback,
    get_user_attribs_callback
)


def get_feature_enabled(request, flag_key):
    enabled = False
    if hasattr(request, 'optimizely_client'):
        client = request.optimizely_client.get_client()
        if client:
            user_id = get_user_id_callback(request)
            attributes = get_user_attribs_callback(request)
            enabled = client.is_feature_enabled(flag_key, user_id, attributes)
    return enabled
