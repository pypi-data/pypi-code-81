# Generated by Django 3.1.1 on 2021-04-07 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appchance_redlink", '0003_sentpush'),
    ]

    operations = [
        migrations.AddField(
            model_name="sentpush",
            name="body",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="sentpush",
            name="title",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="sentpush",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
    ]
