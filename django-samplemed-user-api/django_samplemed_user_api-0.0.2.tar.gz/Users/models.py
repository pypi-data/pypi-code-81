from django.db import models


# Create your models here.
class Users(models.Model):
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=130)
    name = models.CharField(max_length=255)
    email = models.ManyToManyField('EmailNotificationTypesU')  # many to many from Email_notification_types model
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    # company_id =
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    theme_id = models.ForeignKey('Theme', on_delete=models.CASCADE)  # relationship from Theme entity/model
    failed_login_attempt_count = models.SmallIntegerField()
    status = models.SmallIntegerField()
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserMeta(models.Model):
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    meta_key = models.CharField(max_length=128)

    # meta_value = amount about the JSON value ?? ask

    def __str__(self):
        return '{0}'.format(self.user_id)


class UserPasswordT(models.Model):  # understand whether it proper connected
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.user_id)


"""these models are related from applications (other layer)"""


# class UserDownloadsT(models.Model):
# id = models.IntegerField(auto_increment=True, primary_key=True)
# upload_id = models.ForeignKey() # Applications app <==
# applicant_id = models.ForeignKey() # Applications app <==
# user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
# ip =models.CharField(max_length=255)
# created = models.DateTimeField()

# class GroupsUs(models.Model):
# id = models.IntegerField(auto_increment=True, primary_key=True)
# group_id = models.ForeignKey() ??
# user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


# first
class EmailNotificationTypesU(models.Model):  # needs to upgrade the name
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    email_notification_type_id = models.ForeignKey('EmailNotificationTypeT', on_delete=models.CASCADE)

    def __str__(self):
        # stringfy an int, since it is str
        return '{0}'.format(self.user_id)


# second
class EmailNotificationTypeT(models.Model):
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# this then relates to Users themes_id (related already)
class Theme(models.Model):
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    name = models.CharField(max_length=32)
    icon = models.CharField(max_length=10)  # not ImageField?
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Category(models.Model):
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    name = models.CharField(max_length=45)
    description = models.TextField()
    two_fa_required = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CategoriesEmailNotification(models.Model):
    # id = models.IntegerField(auto_increment=True, primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    email_notification_id = models.IntegerField()

    def __str__(self):
        return 'Email_notification_id {0}'.format(self.email_notification_id)


class ChangeLog(models.Model):
    snapshot_id = models.ForeignKey('Snapshot', on_delete=models.CASCADE)  # BIGINT(20)
    request_id = models.CharField(max_length=36)  # has to transform to VARCHAR(36)?
    request_path = models.CharField(max_length=256)  # VARCHAR(256)
    action_key = models.CharField(max_length=64)  # VARCHAR(64)
    action_type = models.CharField(max_length=16)  # VARCHAR(16)
    entity_id = models.IntegerField()  # has to add max_length as custom for django INT(10)
    user_id = models.IntegerField()  # has to add max_length as custom for django  INT(10)
    # input_data = JSON ????
    created = models.DateTimeField()  # DATETIME

    def __str__(self):
        return 'request_id {0}'.format(self.request_id)


"""
This model is an middle man used to get its id by:
Changelog, SnapshootFiles and SnapshootTab models.
"""


class Snapshot(models.Model):
    status = models.CharField(max_length=16)
    is_active = models.SmallIntegerField()  # Boolean ?????
    created = models.DateTimeField()

    def __str__(self):
        return self.status


class SnapshotsFile(models.Model):
    snapshot_id = models.ForeignKey(Snapshot, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    status = models.CharField(max_length=16)
    created = models.DateTimeField()

    def __str__(self):
        return self.name


class SnapshotTable(models.Model):
    snapshot_id = models.ForeignKey(Snapshot, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
