# Generated by Django 4.1.2 on 2023-09-11 15:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("subscription", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscriptionmodel",
            name="designation_id",
        ),
    ]
