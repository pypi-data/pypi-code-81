"""
使用方法:

    urlpatterns += sso_urls

"""
from django.urls import path

from .views import OAuth2LoginView, LoginSuccessView

__all__ = ["sso_urls"]

sso_urls = [
    path("account/login/", OAuth2LoginView.as_view(), name="login"),
    path("account/login/success/", LoginSuccessView.as_view(), name="login_success"),
]
