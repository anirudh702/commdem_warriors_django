# Generated by Django 4.1.2 on 2023-01-12 07:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("group_challenges", "0002_rulesofgroupchallengemodel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rulesofgroupchallengemodel", name="group_challenge",
        ),
        migrations.CreateModel(
            name="GuidelinesOfGroupChallengeModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(db_index=True, default="", max_length=100)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "group_challenge",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="group_challenges.groupchallengesmodel",
                    ),
                ),
            ],
        ),
    ]