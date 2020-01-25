# Generated by Django 2.2.1 on 2019-11-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("adhesion", "0005_auto_20191112_1021"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventManagement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("date", models.DateField()),
                ("participants_non_adherents", models.IntegerField(default=0)),
                ("max_capacity", models.IntegerField()),
                ("participants", models.ManyToManyField(to="adhesion.Adhesion")),
            ],
        ),
    ]