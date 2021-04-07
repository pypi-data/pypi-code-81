from django.urls import path
from . import views

app_name = 'emails'
urlpatterns = [
    path('send-test/', views.send_test, name='send-test'),
    path('start-scheduling/', views.start_email_scheduler, name='start-scheduling'),
    ]

