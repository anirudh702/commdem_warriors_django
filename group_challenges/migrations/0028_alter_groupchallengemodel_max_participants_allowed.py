# Generated by Django 4.1.2 on 2023-10-01 04:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "group_challenges",
            "0027_groupchallengemodel_groupchallengespaymentmodel_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupchallengemodel",
            name="max_participants_allowed",
            field=models.IntegerField(default=0),
        ),
    ]
