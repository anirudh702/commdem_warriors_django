# Generated by Django 4.1.2 on 2023-01-17 11:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commitment", "0005_alter_usernumberofcommitmentfornextweekmodel_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usernumberofcommitmentfornextweekmodel",
            name="end_date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 1, 22, 17, 21, 11, 934065)
            ),
        ),
    ]
