# Generated by Django 4.1.2 on 2023-01-04 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_alter_subscriptionmodel_designation_id'),
        ('user', '0012_delete_individualexercisemodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpaymentdetailsmodel',
            name='subscription_id',
        ),
        migrations.RemoveField(
            model_name='usersubscriptiondetailsmodel',
            name='subscription_id',
        ),
        migrations.AddField(
            model_name='userpaymentdetailsmodel',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subscription.subscriptionmodel'),
        ),
        migrations.AddField(
            model_name='usersubscriptiondetailsmodel',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subscription.subscriptionmodel'),
        ),
    ]