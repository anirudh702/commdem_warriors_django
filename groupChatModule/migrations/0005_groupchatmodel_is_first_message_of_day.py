# Generated by Django 4.1.2 on 2023-04-09 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupChatModule', '0004_alter_groupchatmodel_files_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupchatmodel',
            name='is_first_message_of_day',
            field=models.BooleanField(default=False),
        ),
    ]