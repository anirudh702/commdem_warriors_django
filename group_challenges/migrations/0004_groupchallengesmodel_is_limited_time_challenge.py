# Generated by Django 4.1.2 on 2023-08-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "group_challenges",
            "0003_rename_end_date_groupchallengesmodel_challenge_date_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="groupchallengesmodel",
            name="is_limited_time_challenge",
            field=models.BooleanField(default=False),
        ),
    ]
