# Generated by Django 4.1.2 on 2023-01-08 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0007_workoutwisechallengesmodel_workout_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutwisechallengesmodel',
            name='challenge_name',
            field=models.CharField(db_index=True, default='', max_length=80, unique=True),
        ),
    ]