# Generated by Django 4.1.2 on 2023-04-15 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_usermodel_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]