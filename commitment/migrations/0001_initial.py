# Generated by Django 4.1.2 on 2022-12-07 16:33

import commitment.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CauseOfCategorySuccessOrFailureModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200, unique=True)),
                ('is_success', models.BooleanField()),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='CommitmentCategoryModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='CommitmentGraphDataModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, default=0)),
                ('percentage_done', models.FloatField()),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='CommitmentModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, default=0)),
                ('commitment_date', models.DateTimeField(blank=True, default=commitment.models.next_day_datetime)),
                ('is_done', models.BooleanField(default=False)),
                ('is_updated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentcategorymodel')),
            ],
        ),
        migrations.CreateModel(
            name='ReasonBehindCommitmentSuccessOrFailureForUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, default=0)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('cause_of_category_success_or_failure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commitment.causeofcategorysuccessorfailuremodel')),
                ('commitment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CommitmentNameModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
                ('successName', models.CharField(db_index=True, max_length=200, unique=True)),
                ('failureName', models.CharField(db_index=True, max_length=200, unique=True)),
                ('currentDayName', models.CharField(db_index=True, max_length=200, unique=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentcategorymodel')),
            ],
        ),
        migrations.AddField(
            model_name='commitmentmodel',
            name='commitment_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentnamemodel'),
        ),
        migrations.AddField(
            model_name='causeofcategorysuccessorfailuremodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentcategorymodel'),
        ),
    ]
