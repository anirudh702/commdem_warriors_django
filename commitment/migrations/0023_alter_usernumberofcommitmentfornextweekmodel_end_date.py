# Generated by Django 4.1.2 on 2023-01-06 04:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commitment", "0022_alter_usernumberofcommitmentfornextweekmodel_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usernumberofcommitmentfornextweekmodel",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 1, 8, 9, 53, 47, 490969)
            ),
        ),
    ]
