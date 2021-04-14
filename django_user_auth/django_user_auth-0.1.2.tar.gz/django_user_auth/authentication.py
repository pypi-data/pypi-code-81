from datetime import timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework import  exceptions
from django.utils import timezone
from django.conf import settings

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    扩展Token验证是增加过期时间的判断
    """
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(('Invalid token.'))
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(('User inactive or deleted.'))
        elif timezone.now() > (token.created + timedelta(seconds=settings.SESSION_COOKIE_AGE)):
            #如果当前的时间大于Token创建时间+7天，那么久返回Token已经过期
            raise exceptions.AuthenticationFailed(('Token has expired'))
        return (token.user, token)
