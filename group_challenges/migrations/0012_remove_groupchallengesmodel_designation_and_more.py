# Generated by Django 4.1.2 on 2023-09-11 15:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("group_challenges", "0011_groupchallengesmodel_subscription"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="designation",
        ),
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="gender",
        ),
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="max_age",
        ),
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="max_rating",
        ),
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="min_age",
        ),
        migrations.RemoveField(
            model_name="groupchallengesmodel",
            name="min_rating",
        ),
    ]