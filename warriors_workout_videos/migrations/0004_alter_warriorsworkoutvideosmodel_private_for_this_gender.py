# Generated by Django 4.1.2 on 2023-08-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "warriors_workout_videos",
            "0003_alter_warriorsworkoutvideosmodel_is_private_for_all_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="warriorsworkoutvideosmodel",
            name="private_for_this_gender",
            field=models.CharField(blank=True, default="", max_length=10, null=True),
        ),
    ]