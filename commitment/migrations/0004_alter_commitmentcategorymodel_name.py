# Generated by Django 4.1.2 on 2022-10-19 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0003_rename_commitment_name_commitmentmodel_commitment_name_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitmentcategorymodel',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
