# Generated by Django 4.1.2 on 2022-12-11 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_delete_keystoupdateinfrontendmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='keysToUpdateInFrontEndModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_new_commitment_category_added', models.BooleanField(default=False)),
            ],
        ),
    ]
