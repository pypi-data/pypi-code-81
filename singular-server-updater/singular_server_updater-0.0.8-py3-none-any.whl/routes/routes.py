from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from singular_server_updater.webhooks.webhooks import PushRequest

urlpatterns = [
    url('webhooks/push_request', csrf_exempt(PushRequest.as_view()))
]
