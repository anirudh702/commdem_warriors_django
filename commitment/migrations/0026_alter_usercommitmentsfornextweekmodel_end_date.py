# Generated by Django 4.1.2 on 2023-04-17 23:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0025_remove_exercisemodel_positive_affirmations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommitmentsfornextweekmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 23, 5, 6, 25, 353367)),
        ),
    ]
