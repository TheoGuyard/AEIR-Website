# Generated by Django 3.0.1 on 2020-01-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0010_globalwebsiteparameters_sell_conditions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="globalwebsiteparameters",
            name="sell_conditions",
            field=models.FileField(default=None, upload_to="global_parameters"),
        ),
    ]