# Generated by Django 2.2.1 on 2019-12-25 10:09

from django.db import migrations
import stdimage.models
import stdimage.validators


class Migration(migrations.Migration):

    dependencies = [
        ("adhesion", "0006_auto_20191213_1717"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adhesion",
            name="picture",
            field=stdimage.models.StdImageField(
                upload_to="adhesion_aeir",
                validators=[
                    stdimage.validators.MinSizeValidator(800, 600),
                    stdimage.validators.MaxSizeValidator(1080, 720),
                ],
            ),
        ),
    ]