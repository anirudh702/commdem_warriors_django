# Generated by Django 4.1.2 on 2023-10-02 16:52

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "soloCompetitionsForFreeTrialUsers",
            "0028_alter_freetrialsolochallengesmodel_challenge_date",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="freetrialsolochallengesmodel",
            name="challenge_date",
            field=models.DateField(blank=True, default=datetime.date(2023, 10, 12)),
        ),
    ]
