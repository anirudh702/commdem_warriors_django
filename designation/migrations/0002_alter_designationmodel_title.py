# Generated by Django 4.1.2 on 2022-12-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designationmodel',
            name='title',
            field=models.CharField(max_length=100, unique=True,db_index=True),
        ),
    ]
