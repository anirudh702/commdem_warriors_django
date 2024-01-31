# Generated by Django 4.1.2 on 2023-07-29 06:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("commitment", "0004_alter_usercommitmentsfornextweekmodel_end_date"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RulesOfSoloChallengesModel",
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
            ],
        ),
        migrations.CreateModel(
            name="WorkoutSuggestionsForSoloChallengeModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "workout_name",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commitment.commitmentnamemodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FreeTrialSoloChallengesModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "challenge_name",
                    models.CharField(db_index=True, max_length=80, unique=True),
                ),
                (
                    "challenge_video_url",
                    models.CharField(db_index=True, max_length=80, unique=True),
                ),
                (
                    "challenge_title",
                    models.CharField(db_index=True, default="", max_length=80),
                ),
                ("challenge_image", models.FileField(blank=True, upload_to="")),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "suggested_workout",
                    models.ManyToManyField(to="commitment.commitmentnamemodel"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="User",
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
    ]