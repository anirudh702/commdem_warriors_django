# Generated by Django 4.1.2 on 2022-12-24 05:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commitment', '0001_initial'),
        ('voiceAssistant', '0007_voiceassistantmessagemodel_is_listening_today'),
    ]

    operations = [
        migrations.CreateModel(
            name='voiceAssistantAfterUpdateMessageModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('no_of_week_from_date_of_joining', models.IntegerField(blank=True, default=0)),
                ('no_of_times_in_current_week', models.IntegerField(blank=True, default=0)),
                ('range_of_success_of_commitment_name', models.CharField(blank=True, max_length=100)),
                ('range_of_current_week_success_of_commitment_category', models.CharField(blank=True, max_length=100)),
                ('is_it_weekend', models.BooleanField(default=True)),
                ('voice_assistant_message', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('commitment_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentcategorymodel')),
                ('commitment_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentnamemodel')),
                ('reason_behind_commitment_success_or_failure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.reasonbehindcommitmentsuccessorfailureforuser')),
            ],
        ),
        migrations.CreateModel(
            name='voiceAssistantBeforeUpdateMessageModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('no_of_week_from_date_of_joining', models.IntegerField(blank=True, default=0)),
                ('no_of_times_in_current_week', models.IntegerField(blank=True, default=0)),
                ('range_of_success_of_commitment_name', models.CharField(blank=True, max_length=100)),
                ('is_it_weekend', models.BooleanField(default=True)),
                ('voice_assistant_message', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('commitment_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentcategorymodel')),
                ('commitment_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commitment.commitmentnamemodel')),
            ],
        ),
        migrations.DeleteModel(
            name='voiceAssistantMessageModel',
        ),
    ]
