# Generated by Django 4.1.2 on 2023-07-29 07:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("group_challenges", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupchallengesmodel",
            name="is_for_free_trial",
            field=models.BooleanField(default=False),
        ),
    ]
