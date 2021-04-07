# Generated by Django 2.2.15 on 2020-10-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flow", "0046_purge_data_dependencies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datadependency",
            name="kind",
            field=models.CharField(
                choices=[
                    ("io", "Input/output dependency"),
                    ("subprocess", "Subprocess"),
                    ("duplicate", "Duplicate"),
                ],
                max_length=16,
            ),
        ),
    ]
