# Generated by Django 4.1.2 on 2023-08-04 15:19

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("commitment", "0007_alter_usercommitmentsfornextweekmodel_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercommitmentsfornextweekmodel",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 8, 6, 15, 19, 18, 278715)
            ),
        ),
    ]
