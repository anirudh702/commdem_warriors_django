# Generated by Django 4.1.2 on 2023-04-09 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges_result', '0002_challengesresultmodel_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengesresultmodel',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
    ]
