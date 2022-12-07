# Generated by Django 4.1.2 on 2022-12-06 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_usermodel_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergooglesigninmodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userhealthdetailsmodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userlocationdetailsmodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofessionaldetailsmodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]