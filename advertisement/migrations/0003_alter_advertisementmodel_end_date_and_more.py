# Generated by Django 4.1.2 on 2023-04-08 08:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_alter_advertisementmodel_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementmodel',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 15, 14, 3, 35, 98588)),
        ),
        migrations.AlterField(
            model_name='advertisementmodel',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 9, 14, 3, 35, 98563)),
        ),
    ]