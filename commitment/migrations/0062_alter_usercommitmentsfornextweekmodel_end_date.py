# Generated by Django 4.1.2 on 2023-10-01 10:51

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("commitment", "0061_alter_usercommitmentsfornextweekmodel_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercommitmentsfornextweekmodel",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 10, 8, 10, 51, 3, 797154)
            ),
        ),
    ]
