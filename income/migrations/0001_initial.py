# Generated by Django 4.1.2 on 2023-07-29 06:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IncomeModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("income_range", models.CharField(max_length=100)),
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
    ]
