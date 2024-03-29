# Generated by Django 4.1.2 on 2022-12-05 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='causeofcategorysuccessorfailuremodel',
            name='is_success',
            field=models.BooleanField(db_index=True),
        ),
        migrations.AlterField(
            model_name='causeofcategorysuccessorfailuremodel',
            name='title',
            field=models.CharField(max_length=200, unique=True,db_index=True),
        ),
        migrations.AlterField(
            model_name='commitmentcategorymodel',
            name='name',
            field=models.CharField( max_length=200, unique=True,db_index=True),
        ),
        migrations.AlterField(
            model_name='commitmentgraphdatamodel',
            name='created_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='commitmentgraphdatamodel',
            name='percentage_done',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='commitmentgraphdatamodel',
            name='updated_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='commitmentgraphdatamodel',
            name='user_id',
            field=models.IntegerField(blank=True, db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='commitmentmodel',
            name='created_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='commitmentmodel',
            name='is_done',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='commitmentmodel',
            name='is_updated',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='commitmentmodel',
            name='updated_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='commitmentnamemodel',
            name='currentDayName',
            field=models.CharField(max_length=200, unique=True,db_index=True),
        ),
        migrations.AlterField(
            model_name='commitmentnamemodel',
            name='failureName',
            field=models.CharField(max_length=200, unique=True,db_index=True),
        ),
        migrations.AlterField(
            model_name='commitmentnamemodel',
            name='name',
            field=models.CharField(max_length=200, unique=True,db_index=True),
        ),
        migrations.AlterField(
            model_name='commitmentnamemodel',
            name='successName',
            field=models.CharField(max_length=200, unique=True,db_index=True),
        ),
        migrations.AlterField(
            model_name='reasonbehindcommitmentsuccessorfailureforuser',
            name='created_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reasonbehindcommitmentsuccessorfailureforuser',
            name='updated_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reasonbehindcommitmentsuccessorfailureforuser',
            name='user_id',
            field=models.IntegerField(blank=True, db_index=True, default=0),
        ),
    ]
