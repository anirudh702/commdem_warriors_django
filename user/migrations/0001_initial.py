# Generated by Django 4.1.2 on 2023-01-11 05:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("designation", "0001_initial"),
        ("income", "0001_initial"),
        ("subscription", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="keysToUpdateInFrontEndModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "is_new_commitment_category_added",
                    models.BooleanField(default=False),
                ),
                ("is_commitment_table_updated", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="UserCashbackModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("user_id", models.IntegerField(blank=True, default=0)),
                ("amount", models.FloatField(blank=True, default=0.0)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=100)),
                (
                    "mobile_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        db_index=True,
                        error_messages={
                            "unique": "This mobile number already exists in our database"
                        },
                        max_length=128,
                        region=None,
                        unique=True,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        db_index=True,
                        error_messages={
                            "unique": "This Email already exists in our database"
                        },
                        max_length=254,
                        null=True,
                        unique=True,
                    ),
                ),
                ("profile_pic", models.FileField(blank=True, upload_to="")),
                ("birth_date", models.DateField(default=django.utils.timezone.now)),
                ("password", models.CharField(blank=True, default="", max_length=50)),
                ("is_subscribed", models.BooleanField(default=False)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "joining_date",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="UserSubscriptionDetailsModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "subscription",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subscription.subscriptionmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfessionalDetailsModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("designation_title", models.CharField(default="", max_length=50)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "designation",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="designation.designationmodel",
                    ),
                ),
                (
                    "income_range",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="income.incomemodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPrivacyModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_age_hidden", models.BooleanField(default=True)),
                ("is_city_hidden", models.BooleanField(default=True)),
                ("is_mobile_number_hidden", models.BooleanField(default=True)),
                ("is_designation_title_hidden", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPaymentDetailsModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("payment_id", models.CharField(max_length=50)),
                (
                    "date_of_payment",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "subscription",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subscription.subscriptionmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserLocationDetailsModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("state_id", models.IntegerField(blank=True, default=0)),
                ("city_id", models.IntegerField(blank=True, default=0)),
                ("city_name", models.CharField(default="", max_length=200)),
                ("country_id", models.IntegerField(blank=True, default=0)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserHealthDetailsModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("weight", models.FloatField(blank=True, default=0.0)),
                ("height", models.IntegerField(blank=True, default=0)),
                ("gender", models.CharField(max_length=30)),
                ("age", models.BigIntegerField()),
                ("is_medicine_ongoing", models.BooleanField(default=False)),
                ("any_health_issues", models.BooleanField(default=False)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserGoogleSignInModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("gmail_id", models.EmailField(max_length=254)),
                ("uid", models.CharField(max_length=200)),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.usermodel",
                    ),
                ),
            ],
        ),
    ]
