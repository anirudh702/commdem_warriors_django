# Generated by Django 4.1.2 on 2022-12-30 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0004_exercisemodel_did_speak_before'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisemodel',
            name='did_speak_positive_affirmation',
            field=models.BooleanField(default=False),
        ),
    ]
