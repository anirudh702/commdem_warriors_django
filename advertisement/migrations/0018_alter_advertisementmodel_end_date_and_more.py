# Generated by Django 4.1.2 on 2023-04-15 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0017_alter_advertisementmodel_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 22, 12, 52, 8, 988962)),
        ),
        migrations.AlterField(
            model_name='advertisementmodel',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 16, 12, 52, 8, 988938)),
        ),
    ]
