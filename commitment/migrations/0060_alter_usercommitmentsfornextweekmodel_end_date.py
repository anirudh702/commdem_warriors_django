# Generated by Django 4.1.2 on 2023-10-01 04:34

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("commitment", "0059_alter_usercommitmentsfornextweekmodel_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercommitmentsfornextweekmodel",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 10, 8, 4, 34, 32, 908541)
            ),
        ),
    ]