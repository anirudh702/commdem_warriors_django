# Generated by Django 4.1.2 on 2022-12-27 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voiceAssistant', '0018_remove_voiceassistantafterupdatemessagemodel_age_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voiceassistantafterupdatemessagemodel',
            name='no_of_times_this_reason_in_current_week',
        ),
    ]