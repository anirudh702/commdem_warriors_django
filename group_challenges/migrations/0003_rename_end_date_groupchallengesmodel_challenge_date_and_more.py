# Generated by Django 4.1.2 on 2023-07-29 07:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("group_challenges", "0002_groupchallengesmodel_is_for_free_trial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="groupchallengesmodel",
            old_name="end_date",
            new_name="challenge_date",
        ),
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="start_date",
        ),
    ]
