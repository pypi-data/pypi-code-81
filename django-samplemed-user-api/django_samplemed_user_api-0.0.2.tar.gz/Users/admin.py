from django.contrib import admin
from .models import Users, UserMeta, UserPasswordT,\
    EmailNotificationTypesU, EmailNotificationTypeT,\
    Theme, Category, CategoriesEmailNotification,\
    Snapshot, SnapshotsFile, SnapshotTable, ChangeLog


# Register your models here.
admin.site.register(Users)

admin.site.register(UserMeta)

admin.site.register(UserPasswordT)

admin.site.register(EmailNotificationTypesU)

admin.site.register(EmailNotificationTypeT)

admin.site.register(Theme)

admin.site.register(Category)

admin.site.register(CategoriesEmailNotification)

admin.site.register(Snapshot)

admin.site.register(SnapshotsFile)

admin.site.register(SnapshotTable)

admin.site.register(ChangeLog)