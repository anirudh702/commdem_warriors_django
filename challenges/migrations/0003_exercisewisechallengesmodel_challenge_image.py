# Generated by Django 4.1.2 on 2023-01-04 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_exercisewisechallengesmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisewisechallengesmodel',
            name='challenge_image',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]