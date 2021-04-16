from django.urls import path

from djoptimizely import views


urlpatterns = [
    path('optimizely/datafile/', views.datafile_webhook, name='optimizely-datafile-webhook'),
]
