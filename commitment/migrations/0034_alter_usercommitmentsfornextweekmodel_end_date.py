# Generated by Django 4.1.2 on 2023-04-20 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0033_alter_usercommitmentsfornextweekmodel_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommitmentsfornextweekmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 23, 16, 48, 3, 449560)),
        ),
    ]
