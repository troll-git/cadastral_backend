# Generated by Django 3.1.3 on 2020-11-23 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0051_pozwoleniageom_point_wkt'),
    ]

    operations = [
        migrations.AddField(
            model_name='wnioskigeom',
            name='point_wkt',
            field=models.CharField(max_length=100, null=True),
        ),
    ]