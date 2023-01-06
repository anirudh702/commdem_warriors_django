# Generated by Django 4.1.2 on 2023-01-04 07:58

import commitment.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0012_alter_usernumberofcommitmentfornextweekmodel_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernumberofcommitmentfornextweekmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 1, 8, 7, 58, 35, 168478)),
        ),
        migrations.AlterField(
            model_name='usernumberofcommitmentfornextweekmodel',
            name='start_date',
            field=models.DateField(blank=True, default=commitment.models.next_day_datetime, error_messages={'unique': 'Data for tomorrow already exists for this user'}),
        ),
    ]