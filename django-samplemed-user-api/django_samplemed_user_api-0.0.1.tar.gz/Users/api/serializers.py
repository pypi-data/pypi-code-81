from rest_framework.serializers import ModelSerializer
from Users.models import Users, UserMeta, UserPasswordT, EmailNotificationTypesU, \
    EmailNotificationTypeT, Theme, Category, CategoriesEmailNotification, \
    Snapshot, SnapshotsFile, SnapshotTable, ChangeLog


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'password',
            'name',
            'email',
            'created',
            'updated',
            'category_id',
            'theme_id',
            'failed_login_attempt_count',
            'status',
            'last_login'
        ]


class UserMetaSerializer(ModelSerializer):
    class Meta:
        model = UserMeta
        fields = [
            'id',
            'user_id',
            'meta_key',
            # 'meta_value'
        ]


class UserPasswordTSerializer(ModelSerializer):
    class Meta:
        model = UserPasswordT
        fields = [
            'id',
            'user_id'
        ]


class EmailNotificationTypesUSerializer(ModelSerializer):
    class Meta:
        model = EmailNotificationTypesU
        fields = [
            'id',
            'user_id',
            'email_notification_type_id'
        ]


class EmailNotificationTypeTSerializer(ModelSerializer):
    class Meta:
        model = EmailNotificationTypeT
        fields = [
            'id',
            'name'
        ]


class ThemeSerializer(ModelSerializer):
    class Meta:
        model = Theme
        fields = [
            'id',
            'icon',
            'title'
        ]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'two_fa_required',
            'created',
            'updated'
        ]


class CategoriesEmailNotificationSerializer(ModelSerializer):
    class Meta:
        model = CategoriesEmailNotification
        fields = [
            'id',
            'category_id',
            'email_notification_id'
        ]


class ChangeLogSerializer(ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = [
            'id',
            'snapshot_id',
            'request_id',
            'request_path',
            'action_key',
            'action_type',
            'entity_id',
            'user_id',
            'created'
        ]


class SnapshotSerializer(ModelSerializer):
    class Meta:
        model = Snapshot
        fields = [
            'id',
            'status',
            'is_active',
            'created'
        ]


class SnapshotsFileSerializer(ModelSerializer):
    class Meta:
        model = SnapshotsFile
        fields = [
            'id',
            'snapshot_id',
            'name',
            'status',
            'created'
        ]


class SnapshotsTableSerializer(ModelSerializer):
    class Meta:
        model = SnapshotTable
        fields = [
            'id',
            'snapshot_id',
            'name'
        ]
