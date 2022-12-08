# Generated by Django 4.1.2 on 2022-12-07 16:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedeemPointsModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('to_user_id', models.IntegerField(blank=True, default=0)),
                ('from_user_id', models.IntegerField(blank=True, default=0)),
                ('redeem_points', models.BigIntegerField()),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
