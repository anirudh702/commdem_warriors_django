# Generated by Django 4.1.2 on 2023-01-05 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_workoutwisechallengesmodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutwisechallengesmodel',
            name='challenge_image',
        ),
        migrations.RemoveField(
            model_name='workoutwisechallengesmodel',
            name='challenge_video_url',
        ),
    ]