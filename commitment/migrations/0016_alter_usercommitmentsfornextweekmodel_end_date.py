# Generated by Django 4.1.2 on 2023-04-15 06:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0015_alter_usercommitmentsfornextweekmodel_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommitmentsfornextweekmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 16, 11, 54, 6, 424593)),
        ),
    ]
