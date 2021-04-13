from django.urls import path

from django.conf import settings
from rest_framework import routers
from Users.api.viewsets import UsersViewSet, UserMetaViewSet, UserPasswordTViewSet, EmailNotificationTypesUViewSet, EmailNotificationTypeTViewSet, \
    ThemeViewSet, CategoryViewSet, CategoryEmailNotificationViewSet, ChangeLogViewSet,\
    SnapshotViewSet, SnapshotFileViewSet, SnapshotTableViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import include

"""
API routes that will be included to the url path
"""

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'user_meta', UserMetaViewSet, basename='user_meta')
router.register(r'user_password_t', UserPasswordTViewSet, basename='user_password_t')
router.register(r'email_notification_type_u', EmailNotificationTypesUViewSet, basename='email_notification_type_u')
router.register(r'email_notification_type_t', EmailNotificationTypeTViewSet, basename='email_notification_type_t')
router.register(r'theme', ThemeViewSet, basename='theme')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'category_email_notification', CategoryEmailNotificationViewSet, basename='category_email_notification')
router.register(r'change_log', ChangeLogViewSet, basename='change_log')
router.register(r'snapshot', SnapshotViewSet, basename='snapshot')
router.register(r'snapshot_file', SnapshotFileViewSet, basename='snapshot_file')
router.register(r'snapshot_table', ThemeViewSet, basename='snapshot_table')


urlpatterns = [
    path('', include(router.urls)),
]