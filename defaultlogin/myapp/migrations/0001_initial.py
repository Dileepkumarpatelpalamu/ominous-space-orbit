# Generated by Django 4.1.7 on 2023-03-28 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("title", models.CharField(blank=True, max_length=50)),
                ("phone", models.CharField(max_length=15)),
                ("email", models.EmailField(max_length=254)),
                ("career", models.TextField(blank=True)),
                ("photo", models.ImageField(blank=True, upload_to="")),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="TechnicalSkill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("database", models.CharField(max_length=100)),
                ("language", models.CharField(max_length=100)),
                ("framework", models.CharField(max_length=100)),
                ("web_technology", models.CharField(max_length=100)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.profile"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Qualification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("degree", models.CharField(max_length=100)),
                ("university", models.CharField(max_length=100)),
                ("pass_out", models.CharField(max_length=20)),
                ("percentage", models.DecimalField(decimal_places=3, max_digits=5)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.profile"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PersonalDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("father_name", models.CharField(max_length=50)),
                ("mother_name", models.CharField(max_length=50)),
                ("permanent_address", models.TextField()),
                ("dob", models.DateField()),
                ("language", models.CharField(max_length=100)),
                ("nationality", models.CharField(max_length=50)),
                ("hobby", models.CharField(max_length=100)),
                ("declare", models.TextField()),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.profile"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PasswordData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=500)),
                ("linkin", models.URLField(blank=True)),
                ("git_link", models.URLField(blank=True)),
                ("wb_link", models.URLField(blank=True)),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.profile"
                    ),
                ),
            ],
        ),
    ]
