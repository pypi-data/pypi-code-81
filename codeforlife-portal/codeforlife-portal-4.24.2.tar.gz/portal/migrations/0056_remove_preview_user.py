# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-08-27 08:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("portal", "0055_add_preview_user")]

    operations = [
        migrations.RemoveField(model_name="userprofile", name="preview_user"),
        migrations.RemoveField(model_name="school", name="eligible_for_testing"),
    ]
