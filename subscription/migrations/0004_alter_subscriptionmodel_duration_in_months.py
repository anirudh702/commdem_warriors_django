# Generated by Django 4.1.2 on 2022-11-12 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_alter_subscriptionmodel_duration_in_months'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionmodel',
            name='duration_in_months',
            field=models.CharField(max_length=100),
        ),
    ]
