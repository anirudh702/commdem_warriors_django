# Generated by Django 4.1.2 on 2023-04-15 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0017_alter_usercommitmentsfornextweekmodel_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommitmentsfornextweekmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 16, 12, 32, 53, 49048)),
        ),
    ]