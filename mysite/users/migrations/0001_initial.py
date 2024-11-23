# Generated by Django 5.0.6 on 2024-07-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                ("username", models.CharField(max_length=150, unique=True)),
                ("email", models.EmailField(max_length=200, unique=True)),
                ("password", models.CharField(max_length=200)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]