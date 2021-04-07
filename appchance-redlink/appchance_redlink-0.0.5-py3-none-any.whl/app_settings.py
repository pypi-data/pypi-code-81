from django.conf import settings

REDLINK_BATCH_SIZE = getattr(settings, "REDLINK_BATCH_SIZE", 100)
REDLINK_DEFAULT_LANGUAGE = getattr(settings, "REDLINK_DEFAULT_LANGUAGE", "en")

REDLINK_APPLICATIONS = [settings.REDLINK_ANDROID_APP_ID, settings.REDLINK_IOS_APP_ID]
