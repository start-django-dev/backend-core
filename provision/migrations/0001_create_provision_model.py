# Generated by Django 3.2.12 on 2022-03-23 03:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("utils", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Provision",
            fields=[
                (
                    "abstractdatetime_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="utils.abstractdatetime",
                    ),
                ),
                (
                    "python_version",
                    models.CharField(max_length=10, verbose_name="Python version"),
                ),
                (
                    "django_version",
                    models.CharField(max_length=10, verbose_name="Django version"),
                ),
                (
                    "project_name",
                    models.CharField(max_length=20, verbose_name="Project name"),
                ),
            ],
            options={
                "verbose_name": "Provision",
                "verbose_name_plural": "Provision List",
                "db_table": "provision",
            },
            bases=("utils.abstractdatetime",),
        ),
    ]
