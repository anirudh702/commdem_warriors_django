# Generated by Django 4.1.2 on 2023-04-08 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0009_alter_usercommitmentsfornextweekmodel_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommitmentsfornextweekmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 9, 16, 36, 2, 844944)),
        ),
    ]
