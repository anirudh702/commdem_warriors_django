# Generated by Django 4.1.2 on 2023-04-09 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_challenges', '0006_alter_groupchallengesmodel_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupchallengesmodel',
            name='max_rating',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='groupchallengesmodel',
            name='min_rating',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
