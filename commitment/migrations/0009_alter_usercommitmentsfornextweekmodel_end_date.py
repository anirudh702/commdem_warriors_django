# Generated by Django 4.1.2 on 2023-08-05 11:25

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("commitment", "0008_alter_usercommitmentsfornextweekmodel_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercommitmentsfornextweekmodel",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 8, 6, 11, 25, 29, 959602)
            ),
        ),
    ]
