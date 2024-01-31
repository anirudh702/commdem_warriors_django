# Generated by Django 4.1.2 on 2023-10-01 10:51

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        (
            "group_challenges",
            "0029_alter_groupchallengemodel_max_participants_allowed",
        ),
        ("user", "0005_userpaymentdetailsmodel_subscription_end_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BiddingContestModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("bid_price", models.IntegerField(default=0)),
                ("max_bids_allowed", models.IntegerField(default=0)),
                ("bids_placed", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
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
                        to="group_challenges.groupchallengemodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionsForBiddingContestModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=300)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "bidding_contest",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bidding_contest.biddingcontestmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParticipantsInBiddingContestModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "bidding_contest",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bidding_contest.biddingcontestmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BiddingContestPaymentModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("payment_id", models.CharField(max_length=50)),
                (
                    "date_of_payment",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "bidding_contest",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bidding_contest.biddingcontestmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AnswersOfBiddingContestModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("answer", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bidding_contest.questionsforbiddingcontestmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
    ]
