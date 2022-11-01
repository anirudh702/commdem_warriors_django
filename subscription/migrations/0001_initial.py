# Generated by Django 4.1.2 on 2022-11-01 12:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount_in_dollars', models.BigIntegerField()),
                ('duration_in_months', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
    ]