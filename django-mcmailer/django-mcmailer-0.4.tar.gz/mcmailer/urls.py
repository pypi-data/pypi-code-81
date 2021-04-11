from django.urls import path

from mcmailer.views import connect_gmail, g_auth_endpoint, send_test_email

app_name = 'mcmailer'
urlpatterns = [
    path('send-test-email/', send_test_email, name='send_test_email'),
    path('connect/', connect_gmail, name='connect_gmail'),
    path('g-auth-endpoint/', g_auth_endpoint, name='g_auth_endpoint'),
]
