# Generated by Django 4.1.2 on 2022-12-17 06:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0005_keystoupdateinfrontendmodel_is_commitment_table_updated"),
    ]

    operations = [
        migrations.CreateModel(
            name="voiceAssistantLanguagesModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("language_name", models.CharField(max_length=30)),
                ("language_code", models.CharField(max_length=5)),
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
            name="userPreferredVoiceLanguageModel",
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
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
                (
                    "voice_assistant_language",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="voiceAssistant.voiceassistantlanguagesmodel",
                    ),
                ),
            ],
        ),
    ]