# Generated by Django 4.1.2 on 2023-04-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges_result', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='challengesresultmodel',
            name='rank',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
