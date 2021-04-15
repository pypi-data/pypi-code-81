from django.conf import settings
from django.utils.timezone import is_aware, make_aware, is_naive, make_naive


def fix_timezone(value, timezone=None, is_dst=None):
    if settings.USE_TZ:
        if not is_aware(value):
            return make_aware(value, timezone=timezone, is_dst=is_dst)
    elif not is_naive(value):
        return make_naive(value, timezone=timezone)
    return value
