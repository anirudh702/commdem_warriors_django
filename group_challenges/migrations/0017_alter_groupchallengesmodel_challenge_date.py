# Generated by Django 4.1.2 on 2023-09-12 18:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "group_challenges",
            "0016_alter_groupchallengesmodel_challenge_video_url_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupchallengesmodel",
            name="challenge_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
