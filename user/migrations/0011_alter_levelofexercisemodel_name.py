# Generated by Django 4.1.2 on 2023-01-03 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_levelofexercisemodel_individualexercisemodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="levelofexercisemodel",
            name="name",
            field=models.CharField(max_length=30),
        ),
    ]