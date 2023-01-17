# Generated by Django 4.1.2 on 2023-01-17 11:39

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0002_userwiseprivacymodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="OneToOneChatModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "chat_message",
                    models.CharField(blank=True, default="", max_length=1000),
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
                    "from_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_user_details",
                        to="user.usermodel",
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OneToOneFilesSharedOnChatModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "path",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), size=None
                    ),
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
                    "chat",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="oneToOneChatModule.onetoonechatmodel",
                    ),
                ),
            ],
        ),
    ]
