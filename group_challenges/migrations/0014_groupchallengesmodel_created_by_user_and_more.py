# Generated by Django 4.1.2 on 2023-09-12 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_alter_usermodel_api_key"),
        (
            "group_challenges",
            "0013_alter_groupchallengesmodel_max_participants_allowed",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="groupchallengesmodel",
            name="created_by_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="user.usermodel",
            ),
        ),
        migrations.AddField(
            model_name="groupchallengesmodel",
            name="is_created_by_user",
            field=models.BooleanField(default=False),
        ),
    ]