# Generated by Django 4.1.2 on 2022-12-27 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiceAssistant', '0019_remove_voiceassistantafterupdatemessagemodel_no_of_times_this_reason_in_current_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voiceassistantafterupdatemessagemodel',
            name='voice_assistant_message',
            field=models.CharField(max_length=400),
        ),
    ]
