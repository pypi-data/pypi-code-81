# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-07-02 08:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aimmo", "0014_add_worksheet_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="worksheet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="aimmo.Worksheet",
            ),
        ),
    ]
