# Generated by Django 4.1.2 on 2023-08-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "warriors_workout_videos",
            "0002_alter_warriorsworkoutvideosmodel_description_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="warriorsworkoutvideosmodel",
            name="is_private_for_all",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="warriorsworkoutvideosmodel",
            name="private_for_this_gender",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]