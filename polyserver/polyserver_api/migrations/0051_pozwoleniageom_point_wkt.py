# Generated by Django 3.1.2 on 2020-11-18 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0050_merge_20201112_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='pozwoleniageom',
            name='point_wkt',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
