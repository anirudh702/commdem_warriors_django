# Generated by Django 4.1.2 on 2022-12-28 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0002_exercisemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisemodel',
            name='time_to_start',
            field=models.CharField(db_index=True, default='', max_length=50),
        ),
    ]