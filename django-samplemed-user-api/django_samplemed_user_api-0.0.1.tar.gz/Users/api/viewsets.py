from rest_framework.viewsets import ModelViewSet
from Users.models import Users, UserMeta, UserPasswordT, EmailNotificationTypesU, \
    EmailNotificationTypeT, Theme, Category, CategoriesEmailNotification, \
    Snapshot, SnapshotsFile, SnapshotTable, ChangeLog

from .serializers import UserSerializer, UserMetaSerializer, UserPasswordTSerializer, \
    EmailNotificationTypesUSerializer, EmailNotificationTypeTSerializer, ThemeSerializer, CategorySerializer, \
    CategoriesEmailNotificationSerializer, ChangeLogSerializer, SnapshotSerializer, SnapshotsFileSerializer, \
    SnapshotsTableSerializer


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserMetaViewSet(ModelViewSet):
    queryset = UserMeta.objects.all()
    serializer_class = UserMetaSerializer


class UserPasswordTViewSet(ModelViewSet):
    queryset = UserPasswordT.objects.all()
    serializer_class = UserPasswordTSerializer


class EmailNotificationTypesUViewSet(ModelViewSet):
    queryset = EmailNotificationTypesU.objects.all()
    serializer_class = EmailNotificationTypesUSerializer


class EmailNotificationTypeTViewSet(ModelViewSet):
    queryset = EmailNotificationTypeT.objects.all()
    serializer_class = EmailNotificationTypeTSerializer


class ThemeViewSet(ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryEmailNotificationViewSet(ModelViewSet):
    queryset = CategoriesEmailNotification.objects.all()
    serializer_class = CategoriesEmailNotificationSerializer


class ChangeLogViewSet(ModelViewSet):
    queryset = ChangeLog.objects.all()
    serializer_class = ChangeLogSerializer


class SnapshotViewSet(ModelViewSet):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer


class SnapshotFileViewSet(ModelViewSet):
    queryset = SnapshotsFile.objects.all()
    serializer_class = SnapshotsFileSerializer


class SnapshotTableViewSet(ModelViewSet):
    query = SnapshotTable.objects.all()
    serializer_class = SnapshotsTableSerializer
