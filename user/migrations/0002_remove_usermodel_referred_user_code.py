# Generated by Django 4.1.2 on 2023-08-23 15:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usermodel",
            name="referred_user_code",
        ),
    ]
