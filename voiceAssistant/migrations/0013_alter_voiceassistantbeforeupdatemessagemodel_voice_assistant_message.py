# Generated by Django 4.1.2 on 2022-12-26 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiceAssistant', '0012_rename_range_of_success_of_commitment_name_voiceassistantbeforeupdatemessagemodel_range_of_success_o'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voiceassistantbeforeupdatemessagemodel',
            name='voice_assistant_message',
            field=models.CharField(max_length=400),
        ),
    ]