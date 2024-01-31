# Generated by Django 4.1.2 on 2023-10-03 02:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "group_challenges",
            "0029_alter_groupchallengemodel_max_participants_allowed",
        ),
        (
            "challenges_result",
            "0003_rename_payment_status_challengesresultmodel_is_payment_done",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="challengesresultmodel",
            name="competition_id",
        ),
        migrations.AddField(
            model_name="challengesresultmodel",
            name="group_challenge",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="group_challenges.groupchallengemodel",
            ),
        ),
    ]