# Generated by Django 2.2.17 on 2021-02-12 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap_success_factors', '0001_squashed_0022_auto_20200206_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='sapsuccessfactorslearnerdatatransmissionaudit',
            name='credit_hours',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
