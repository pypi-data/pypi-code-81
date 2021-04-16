import codecs, hmac

from hashlib import sha1

from django.conf import settings


def verify_signature(request):
    secret = settings.OPTIMIZELY_WEBHOOK_SECRET
    request_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    computed_signature = 'sha1=' + hmac.new(
        codecs.encode(secret),
        msg=request.body,
        digestmod=sha1
    ).hexdigest()
    return hmac.compare_digest(computed_signature, request_signature)
