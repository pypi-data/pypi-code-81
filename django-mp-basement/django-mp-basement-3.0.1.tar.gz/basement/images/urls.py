
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from basement.images import views


app_name = 'images'


urlpatterns = [

    path('upload/<int:content_type_id>/', views.upload_image, name='upload')

]


app_urls = i18n_patterns(
    path('images/', include((urlpatterns, app_name))),
)
