# Generated by Django 2.0 on 2020-10-28 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0059_move_email_verifications_to_common'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guardian',
            name='children',
        ),
        migrations.RemoveField(
            model_name='guardian',
            name='new_user',
        ),
        migrations.RemoveField(
            model_name='guardian',
            name='user',
        ),
        migrations.DeleteModel(
            name='Guardian',
        ),
    ]
