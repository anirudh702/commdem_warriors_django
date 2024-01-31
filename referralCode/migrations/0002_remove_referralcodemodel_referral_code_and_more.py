# Generated by Django 4.1.2 on 2023-08-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("referralCode", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="referralcodemodel",
            name="referral_code",
        ),
        migrations.AddField(
            model_name="referralcodemodel",
            name="referred_user_full_name",
            field=models.CharField(db_index=True, default="", max_length=50),
        ),
        migrations.AddField(
            model_name="referralcodemodel",
            name="referred_user_phone_number",
            field=models.CharField(db_index=True, default="", max_length=15),
        ),
    ]