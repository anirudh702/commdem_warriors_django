# Generated by Django 4.1.2 on 2023-08-07 23:44

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "soloCompetitionsForFreeTrialUsers",
            "0007_alter_freetrialsolochallengesmodel_challenge_date",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="freetrialsolochallengesmodel",
            name="challenge_date",
            field=models.DateField(blank=True, default=datetime.date(2023, 8, 17)),
        ),
    ]
