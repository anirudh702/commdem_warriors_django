# Generated by Django 4.1.2 on 2023-01-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionmodel",
            name="is_call_service_included",
            field=models.BooleanField(default=False),
        ),
    ]
